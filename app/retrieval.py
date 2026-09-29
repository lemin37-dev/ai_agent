'''
- postsql + pgvector를 이용하여 벡터 데이터를 검색, 유사도 체크 등 진행
- 벡터 검색, 메타데이터 필터링, 하이브리드 서치 기능까지 확장
'''

from pgvector import Vector
from app.database import connect
from app.embedding import get_embeddings

def vector_search(query:str, k:int=5):
  # 1. 사용자 질문 임베딩 -> 벡터 변환 처리
  q = Vector(get_embeddings().embed_query(query))

  # 2. Vector DB
  results = None
  with connect() as conn, conn.cursor() as cur:
    # 질문과 chunking 비교하여 유사도 계산
    cur.execute('''
      select
        d.document_code,
        d.title,
        d.department,
        d.category,
        dc.content,
        1-(dc.embedding <=> %s) score
      from 
        document_chunks dc
      join 
        documents d on dc.document_id = d.id
      order by (dc.embedding <=> %s)
      limit %s
    ''', (q, q, k))
    results = cur.fetchall()
  
  return results