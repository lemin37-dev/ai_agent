'''
- Agent가 RAG 기능을 사용하기 위해서 툴로 등록
'''

from langchain_core.tools import tool
from app.retrieval import advanced_search


# 툴로 구성, 등록 절차
# @tool을 함수의 데코레이터 자리에 배치
@tool
def search_company_policy(query:str, department:str="") -> str:
  '''
  사내 HR/CS/Sales 규정과 정책을 검색한다. 해당 내용은 LLM이 한번도 접하지 못한 내용인 사내 정보을 담고 있음.
  부서를 알거나 추정할 수 있다면 HR, CS, Sales 중 하나를 검색 시 반영.
  '''
  rows = advanced_search(query, department=department or None, k=5) # k 값은 에이전트 선택 못하게 고정(변동가능)
  if not rows: return "사내 규정 없음"
  return "\n\n".join(f"[source={row[0]} | hybrid={row[-1]:.3f}]\n{row[4]}" for row in rows) # LLM 추론 시 근거자료로 활용
