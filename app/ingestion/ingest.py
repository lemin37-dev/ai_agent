'''
- 업무 문서를 chunking -> embedding -> PostgreSQL/pgvector 적재
- RAG에서 사용하는 지식 베이스 구성에 대한 Ingestion pipeline
'''

from pathlib import Path
from .loader import load_markdown

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"

# md 파일별 처리 
def ingest_file(path:Path):
    # 1. 문서 내에서 메타데이터와 본문 분리 -> '---' 기준 분할
    meta, body = load_markdown(path)

    pass

def main():
  # 파일별 처리 구성
  for path in sorted(DATA.rglob("*.md")):
    ingest_file(path)
  pass

if __name__ == "__main__":
  main()