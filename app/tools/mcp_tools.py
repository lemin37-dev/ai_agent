'''
- MCP Client
- MCP Server와 통신 담당
- LangGraph의 ToolNoe에 등록
- Agent가 필요하면 도구로 사용
'''

from pathlib import Path
from fastmcp import Client
from langchain_core.tools import tool

# MCP 서버가 백엔드 등에서 구동되어 있지 않으므로, 직접 경로를 접근하여 실행
ROOT = Path(__file__).resolve().parents[2] # Project Root
# 실제 MCP 서버 경로
SERVER = ROOT / "mcp_servers" / "exchange_server.py"

# Tool 구성
@tool
async def get_exchange_rate(base:str="USD", quote:str="KRW") -> str:
  '''
  MCP 서버에서 환율정보 조회.
  단, 실시간 환율은 아님.
  '''
  # MCP Server에 MCP Client 연결
  async with Client(SERVER) as client:
    print("MCP 서버 연결 완료")

    # MCP 서버의 tool 호출
    result = await client.call_tool(
      name = "get_exchange_rate",
      arguments = {
        "base"  : base,
        "quote" : quote
      }
    )

    # 실행결과 반환
    return str(result.data)