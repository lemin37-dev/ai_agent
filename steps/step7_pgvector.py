'''
텍스트 -> 임베딩하여 생성된 벡터 데이터를 PostgreSQL의 pgvector에 저장하고 유사도 검색 SQL 실행
'''

# 1. 모듈 가져오기
from pgvector import Vector
from app.embedding import get_embeddings
from app.database import connect

# 2. 검색어로 사용될만한 샘플 문장 준비 (HR, Sales, CS)
samples = ["환불 정책", "연차 휴가 규정", "월 매출 분석"]

# 3. embedding
vectors = get_embeddings().embed_documents(samples)

# 4. DB load
# with문 2개 사용하는 것과 같은 결과
with connect() as conn, conn.cursor() as cur:
  # 데이터 : 원문 텍스트, 임베딩된 벡터
  for text, vec in zip(samples, vectors):
    # SQL 수행
    cur.execute('''
      insert into demo_vectors(content, embedding) values (%s, %s)
      on conflict(content)
      do update set embedding=EXCLUDED.embedding
    ''', (text, Vector(vec)))

  conn.commit()
  pass

# 5. 유사도 검사 (질문 벡터 <-> DB 상 적재된 데이터 벡터 간 거리를 측정)
# 5-1. 질문의 벡터화
q = get_embeddings().embed_query('상품을 반품하고 싶어요') # CS 관련 질문
with connect() as conn, conn.cursor() as cur:
  # <=> : cosine 유사도 계산 연산자 (pgvecotr 제공)
  # embedding <=> %s : 유사도 측정 표현
  # 계산값이 작으면 서로 비슷함 -> 1 - (계산값) -> 값이 크면 유사도가 높다
  cur.execute('''
    select
      content,
      1-(embedding <=> %s) score
    from
      demo_vectors
    order by
      (embedding <=> %s)
    limit 3
  ''', (Vector(q), Vector(q)))
  # 결과 출력
  for result in cur.fetchall():
    print(result)

