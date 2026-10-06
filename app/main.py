'''
LangGraph 기반 Agent 실행하는 코드
'''

import asyncio
from app.agent.graph import build_graph

# 테스트용/Fastapi/Slack 등 공용
graph = build_graph()

# 에이전트 실행 함수
async def invoke_agent(question:str):
  return await graph.ainvoke(
    {"messages": [("user", question)], "rounds": 0, "final":None, "tool_rounds":0},
    # 최대 순환 횟수 제한
    config = {"recursion_limit": 18}
  )

async def run(query:str):
  '''
  사용자 질문 -> LangGraph 기반 Agent 전달
  '''
  result = await build_graph().ainvoke(
    # messages.user : 사용자의 질문 값 세팅
    # rounds : 초기 0회로 세팅
    {"messages": [("user", query)], "rounds": 0},
    # 최대 순환 횟수 제한
    config = {"recursion_limit": 18}
  )

  # 툴 중심 상태 관리값 추출
  for message in result["messages"]:
    if getattr(message, "tool_calls", None):  # 툴 이름
      print("TOOL CALLS : ", [x.get('name') for x in message.tool_calls])
    if getattr(message, "type", ""):  # 툴 결과
      print("TOOL RESULT : ", message.content)

  # 최종 답변
  final_res = result.get('final')
  print("+"*30)
  print("[최종답변]\n\n", final_res.model_dump_json(indent=2) if final_res else result["messages"][-1].content)
  print("+"*30)