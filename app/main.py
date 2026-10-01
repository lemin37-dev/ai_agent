'''
LangGraph 기반 Agent 실행하는 코드
'''

import asyncio
from app.agent.graph import build_graph

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

  # 전체 맥락(상태 변화 기록)
  print(result["messages"])

  # 최종 답변
  print("+"*30)
  print("[최종답변]\n\n", result["messages"][-1].content)
  print("+"*30)