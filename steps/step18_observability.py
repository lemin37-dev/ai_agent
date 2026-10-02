'''
Agent 실행을 통해 LLM/Tool/LangGraph 등이 실행 -> LangSmith에 Tracing -> 대시보드 모니터링, 분석
'''

import asyncio
from app.main import run
from app.observability import status

query = "상품 자체 하자의 환불조건을 근거와 함께 알려줘."

async def main():
  # LangSmith 상태 체크
  print("[LangSmith Status]", status())

  # Agent 사용
  print("RUN Agent")
  result = await run(query)

  # 결과확인
  print(result)


asyncio.run(
  main()
)
