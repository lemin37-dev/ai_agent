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


def advanced_search(
    query:str,
    department:str | None = None,
    category:str | None = None,
    k:int=5
):
  '''
  - 벡터 검색 + 메타데이터 필터링 + 키워드 결합한 검색 (RDB + 벡터디비 장점 혼용)
  '''
  # 1. 사용자 질문 임베딩 -> 벡터 변환 처리
  q = Vector(get_embeddings().embed_query(query))

  # 2. 필터링 관련, 키워드(파라미터) 모음 리스트
  filters, params = [], []

  # 3. Department 처리
  if department:
    filters.append("d.department=%s")
    params.append(department.upper())

  # 4. Category 처리
  if category:
      filters.append("d.category=%s")
      params.append(category.lower())

  # 5. 조건 쿼리 구성
  where = ("where " + " AND ".join(filters)) if filters else ""

  # 6. SQL 구성
  # PostgreSQL의 FTS(Full Text Search)를 이용한 키워드 일치 점수 산출 기능
  # ts_rank : 문서와 검색어가 얼마나 잘 일치하는지 점수로 계산
  # to_tsvector : 문서 내용을 검색가능한 토큰 형태로 변환. simple : 보편적인 언어 대상 (그 외, english 등 존재)
  # plainto_tsquery : 사용자가 입력한 일반 문자열을 PostgreSQL의 검색 Query 형태로 변환

  # 하이브리드 검색 + 키워드 검색
  # 유사도 점수, FTS 점수를 블렌딩 처리 + 키워드(부서, 카테고리)
  sql = f'''
    with scored as (
        select
          d.document_code,
          d.title,
          d.department,
          d.category,
          dc.content,
          1-(dc.embedding <=> %s) vector_score,
          ts_rank(
            to_tsvector('simple', dc.content),
            plainto_tsquery('simple', %s)
          ) as fts_score
        from 
          document_chunks dc
        join 
          documents d on dc.document_id = d.id
        {where}
    )
    select
      document_code,
      title,
      department,
      category,
      content,
      vector_score,
      (vector_score*0.80 + LEAST(fts_score, 1.0)*0.20) as hybrid_score
    from scored
    order by hybrid_score desc
    limit %s
  '''

  # 7. param 구성
  total_params = [q, query, *params, max(1, min(k, 20))]

  # 8. query 수행
  with connect() as conn, conn.cursor() as cur:
    cur.execute(sql, total_params)
    return cur.fetchall()
