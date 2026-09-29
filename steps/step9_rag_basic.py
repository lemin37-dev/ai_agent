'''
- 기본 RAG
  질문(고정) -> 청크 검색(벡터 디비) -> 유사도 순 랭킹(top k개) -> 프롬프트 + 검색내용 -> LLM 호출
'''
from app.retrieval import vector_search
from app.rag import answer


q = '상품 자체 하자는 언제까지 환불할 수 있나요?'  # 벡터디비 검색 유사도로 CS 관련 정책을 가져오도록 구성(목표)
q = '입사 6개월차 신입 개발자입니다. 연차사용가능한가요?'

print(answer(q))

