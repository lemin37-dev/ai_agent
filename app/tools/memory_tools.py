'''
- @tool이 붙은 함수의 내부의 1번라이에는 함수 주석(doc-string)을 작성하여 함수의 역할을 명확하게 기술 -> LLM이 판단하는 재료
- 도구
  - 사용자가 명시한 지속적인 신호, 업무 방식을 장기기억으로 저장하는 도구(함수)
  - 현재 질문과 관련된 사용자의 과거 장기 기억을 검색하는 도구
'''
from langchain_core.tools import tool
from app.database import connect
from app.embedding import get_embeddings
from app.config import USER_ID
from pgvector import Vector


@tool
def remember_user_prefrence(content:str, importance:float=0.7) -> str:
  '''
  사용자가 명시한 지속적인 신호, 업무 방식을 장기기억으로 저장
  '''
  # 파라미터 구성
  # content 벡터화
  vec = Vector( get_embeddings().embed_query(content) )
  # 중요도 보정
  importance = max(0.0, min(float(importance), 1.0))

  # 쿼리 실행
  with connect() as conn, conn.cursor() as cur:
      # insert 구문
      sql = """
          insert into agent_memories
          (user_id, memory_type, content, embedding, importance)
          values
          (%s,'preference', %s, %s, %s)
      """
      params = (USER_ID, content, vec, importance)
      cur.execute( sql, params )
      conn.commit()

  return "preference memory saved" # 도구를 사용한 LLM에게 전달

@tool
def recall_user_memory(query:str, k:int=3) -> str:
  '''
  현재 질문과 관련된 사용자의 과거 장기 기억을 검색
  '''
  # 파라미터 구성
  q = Vector(get_embeddings().embed_query(query))
  k = max(1, min(k, 5))
  
  # 쿼리 실행
  with connect() as conn, conn.cursor() as cur:
    # 조회
    sql = '''
      select
        id, memory_type, content, importance,
        1-(embedding <=> %s) as score
      from agent_memories
      where user_id=%s
      order by embedding <=> %s
      limit %s
    '''
    params = (q, USER_ID, q, k)
    cur.execute(sql, params)
    rows = cur.fetchall()
    # memory access 시간 update
    if rows:
       cur.execute('''
        update
          agent_memories
        set 
          last_accessed_at=NOW()
        where 
          id=ANY(%s)
       ''', ([row[0] for row in rows],))

    conn.commit()

  return "\n".join(f"[{type} | score={score:.3f} | importance={importance}] {content}" for _, type, content, importance, score in rows) or "관련 기억 없음"