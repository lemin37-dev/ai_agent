'''
- LangGraph 구성
- Agent 구성
- LangGraph에 agent, tools 등을 등록, 순서 지정, 사용가능한 형태로 빌드
'''
# 필요 모듈 획득
from langchain_core.messages import SystemMessage # Agent 구성 시 System 프롬프트에 해당
from langgraph.graph import StateGraph, START, END # LangGraph의 구성요소
from langgraph.prebuilt import ToolNode, tools_condition # Tool 실행, 호출여부 판단
from app.llm import get_chat_model # LLM 모델
from app.agent.state import AgentState # LangGraph 상에서 상태 관리용
from app.agent.prompts import SYSTEM_PROMPT # 미리 작성해둔 System Prompt 활용
from app.tools.sql_tools import sales_summary, top_products, refund_summary # SQL Tool
from app.tools.rag_tools import search_company_policy # LAG Tool
from app.tools.memory_tools import remember_user_prefrence, recall_user_memory # Memroy Tool
from app.tools.mcp_tools import get_exchange_rate # MCP Tool

# 툴 목록 구성
TOOLS = [sales_summary, top_products, refund_summary, search_company_policy, remember_user_prefrence, recall_user_memory, get_exchange_rate]

# 그래프 빌드
def build_graph():
  # 추론을 담당하는 LLM
  model = get_chat_model()
  # 도구를 사용하는 LLM
  bind_model = model.bind_tools(TOOLS)

  # Agent 노드 -> 추론 or 도구+추론
  async def call_model(state:AgentState):
    # 라운드 값 획득 (LangGraph 내에서 순환 횟수 -> 추론 횟수)
    rounds = state.get('rounds', 0)
    # 라운드를 기점으로 모델을 선택 -> 6회 미만일 때만 도구를 사용한 추론
    select_model = model if rounds >= 6 else bind_model
    # 비동기 추론 호출 -> invoke : 동기식 / ainovke : 비동기식
    response = await select_model.ainvoke(
      # 도구를 사용했다면 or 첫번째가 아니라면 messages에 기록이 존재함 -> 따라서, 그간 추론하고 행동한 모든 내역을 같이 보냄
      [SystemMessage(content=SYSTEM_PROMPT), *state['messages']]
    )
    # 추론 결과, 라운드(LLM 1회 호출) + 1 반환 -> state['messages']에 기록 -> 상태 관리
    return {"messages":[response], "rounds": rounds+1}

  # 그래프 생성
  graph = StateGraph(AgentState)  # 상태 정보를 가진 그래프 생성

  # 노드 등록 (LLM 추론, 도구)
  graph.add_node("agent", call_model)
  # handle_tool_errors : 툴 실행 중에 에러 발생 시 에이전트 전체를 바로 실패시키지 않고 오류를 처리하여 Agent가 대응하게 할 것인지 여부
  graph.add_node("tools", ToolNode(TOOLS, handle_tool_errors=True))

  # 흐름 구성
  # add_edge("A", "B") : A -> B
  # 시작점 
  graph.add_edge(START, "agent")
  # 조건부 실행 (Agent가 툴이 필요한 경우 or 아닐 경우 END로 이동 -> 추론을 통해 판단)
  '''
             tools_condition
                   │
          ┌────────┴────────┐
          ↓                 ↓
      "tools"              END       <- tools_condition 함수의 반환값
          │                 │
          ↓                 ↓
     tools 노드            END (종료) <- 이동할 노드
  '''
  graph.add_conditional_edges("agent", tools_condition, {"tools":"tools", END:END})
  # 툴 사용 이후 방향성 
  graph.add_edge("tools", "agent")

  # 그래프 컴파일 및 반환
  return graph.compile()
