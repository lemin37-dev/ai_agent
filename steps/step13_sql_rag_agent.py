import asyncio
from app.main import run

query = "2026년 9월 1일 부터 2026년 9월 5일까지 환불 현황을 확인하고, 상품 하자 환불 정책을 함께 설명해줘."

asyncio.run(
  run(query)
)
