'''
- 당일 환율 요청하면 응답
- 환율 API 제공해주는 업체와 연동하여 MCP Client 요청 시 응답하는 구조로 특정 클라우드 등 서버에 위치한다
'''
from fastmcp import FastMCP

# FastMCP 생성
mcp = FastMCP("exchange-mcp")

# LLM 에서 호출 시 응답할 MCP Tool 구성
@mcp.tool
def get_exchange_rate(base:str="USD", quote:str="KRW") -> dict:
  '''
  임시용. 고정값으로 응답(실시간 환율 정보 X)
  '''
  rates = {
    ("USD","KRW"): 1364.30,
    ("EUR","KRW"): 1533.61,
    ("JPY","KRW"): 863.24,
  }
  # 키 구성
  key = (base.upper(),quote.upper())

  # 미지원 통화 예외처리
  if not key in rates:
    print(key)
    raise ValueError("미지원 통화")

  # tool의 결과 반환
  return {
    "base" : key[0],
    "quote": key[1],
    "rate" : rates[key],
    "meta" : "dummy-exchange-rate"
  }

if __name__ == '__main__':
  mcp.run()
  