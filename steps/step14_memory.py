'''
사용자의 신호, 습관, 업무형태 등을 기억하게 지시 -> 이를 기억하는지 확인
'''
import asyncio
from app.main import run

async def demo():
  # 명시적 기억 요청
  await run("앞으로 답변은 짧은 bullet 형태를 선호한다. 이 선호를 기억해라.")

  # 확인
  await run("내가 선호하는 답변 방식이 무엇이지?")


asyncio.run(demo())
