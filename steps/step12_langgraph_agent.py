'''
사용자의 질문을 LangGraph에 전달하여 Agent가 처리하도록 테스트
'''
import asyncio
from app.main import run

query = "상품 하자로 반품할 경우 환불 기간과 배송비 부담 주체를 알려주세요."
query = "2026년 9월 1일 부터 2026년 9월 5일까지 매출과 상위 3개 상품을 알려줘."

asyncio.run(
  run(query)
)
