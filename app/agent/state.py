'''
- LangGraph 구성 시 노드들이 등록됨
- 노드 사이에 공유할 Agent 상태 스키마 제공
- 메세지, tool 반복 사용횟수, 최종 구조화 응답 상태 등등 관리
'''

# MessagesState를 상속받은 클래스는 LangGraph의 상태관리 용으로 사용가능함
from langgraph.graph import MessagesState
from app.output import AgentResponse

class AgentState(MessagesState):
  # 라운드 정보만 우선 구성
  rounds:int
  # 최종 구조화된 응답
  final:AgentResponse | None