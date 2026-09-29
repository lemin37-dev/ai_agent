'''
검색된 사내 문서를 근거로 LLM 답변을 생성하는 RAG 모듈
'''
from langchain_core.prompts import ChatPromptTemplate
from app.llm import get_chat_model
from app.retrieval import vector_search

def answer(query:str) -> str:
  # langchain 활용하여 체인 구성 -> LLM 추론 처리
  # 1. 질문에 가장 유사한 사내 규정 5개(default) 획득
  results = vector_search(query)

  # 2. 검색결과를 LLM 프롬프트에 적용할 수 있게 구조 조정
  evidence = '\n\n'.join(f"[{code}] {content}" for code, _, _, _, content, _ in results)

  # 3. prompt 구성
  #    검색된 근거 밖의 내용으로는 답변을 만들지 않도록 제한 추가
  prompt = ChatPromptTemplate.from_messages([
    ("system", "회사의 정책 상담사입니다. 제공된 근거만 사용하고, 답변 끝에 문서 코드를 표시하세요. 근거가 부족하면 모른다고 답하세요."),  
    ("human", "질문: {query}\n\n근거:\n{evidence}"),
  ])

  # 4. 체인 구성 -> LLM 호출 -> 응답 획득
  return (prompt | get_chat_model()).invoke({"query":query, "evidence":evidence}).content
