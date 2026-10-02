'''
MCP Host 역할 (실제 만들고자하는 앱/서비스)
'''

import asyncio
from app.main import run

async def demo():
  await run("달러 대비 원화 환율을 확인해줘.")

  #await run("위안화 대비 원화 환율을 확인해줘.")

asyncio.run(demo())
