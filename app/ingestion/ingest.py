'''
- 업무 문서를 chunking -> embedding -> PostgreSQL/pgvector 적재
- RAG에서 사용하는 지식 베이스 구성에 대한 Ingestion pipeline
'''

from pathlib import Path
from .loader import load_markdown
from .splitter import split_text
from app.embedding import get_embeddings
from app.database import connect
from pgvector import Vector
from psycopg.types.json import Jsonb

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"

# md 파일별 처리 
def ingest_file(path:Path):
    # 1. 문서 내에서 메타데이터와 본문 분리 -> '---' 기준 분할
    meta, body = load_markdown(path)
    # 2. body(본문) 관련 RAG에서 검색 가능한 작은 단위로 chunk 처리
    chunks = split_text(body)
    # 3. 임베딩 처리
    vectors = get_embeddings().embed_documents(chunks)
    # 4. 메타데이터, 벡터를 데이터베이스에 입력 -> 하나의 트랜잭션으로 관리
    with connect() as conn, conn.cursor() as cur:
       # document 저장(1)
       cur.execute('''
        insert into documents
          (document_code, department, category, title, source, version, effective_date)
        values
          (%s, %s, %s, %s, %s, %s, %s)
        on conflict(document_code)
        do update set
          department=EXCLUDED.department,
          category=EXCLUDED.category,
          title=EXCLUDED.title,
          source=EXCLUDED.source,
          version=EXCLUDED.version,
          effective_date=EXCLUDED.effective_date
        returning id
       ''', (meta['document_code'], meta['department'], meta['category'], meta['title'], str(path.relative_to(ROOT)), meta.get('version'), meta.get('effective_date')))
       # 참조키
       document_id = cur.fetchone()[0]

       # 같은 문서로 저장된 청크가 존재한다면 삭제
       cur.execute('delete from document_chunks where document_id=%s', (document_id,))

       # chunks 저장(n)
       for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
          chunk_meta = {
             "section_source": path.name,
             "department": meta['department'],
             "category": meta['category']
          }
          cur.execute('''
            insert into document_chunks
              (document_id, chunk_index, content, embedding, metadata)
            values
              (%s, %s, %s, %s, %s)
          ''', (document_id, i, chunk, Vector(vector), Jsonb(chunk_meta)))

       conn.commit()
       
    pass

def main():
  # 파일별 처리 구성
  for path in sorted(DATA.rglob("*.md")):
    ingest_file(path)
  pass

if __name__ == "__main__":
  main()