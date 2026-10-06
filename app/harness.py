'''
- Agent가 툴 사용 시 제한사항, 정책 등 반영
'''

# 리소스 한도 -> dataclass 데코레이터
from dataclasses import dataclass
# 시간 한도
import time

# 툴 사용한도 -> 툴 사용 목록 제한
ALLOWED_TOOLS = {"sales_summary", "top_products", "refund_summary", 
                 "search_company_policy", 
                 "remember_user_prefrence", "recall_user_memory", 
                 "get_exchange_rate"}

# 에이전트 실행 시 허용할 한도 -> 값으로 세팅
@dataclass
class Limits:
  max_tool_rounds:int = 6   # 최대 tool 실행 라운드
  max_seconds:float = 120.0 # 최대 전체 실행 시간(초단위)

# 에이전트가 사전에 정한 한도를 넘지 않도록 관리
class Budget:
  # 생성자 : 멤버 변수 초기화 진행(초기값 설정)
  def __init__(self,
              tool_rounds:int=0,
              start_at:float|None=None, 
              limits:Limits|None=None):
    # instance 세팅
    self.limits = limits or Limits()
    # 정확한 시간 측정을 위해서 프로그램에 영향을 받지 않는 함수 사용
    self.started = start_at or time.monotonic()
    # 툴 사용 라운드 관리
    self.tool_rounds = tool_rounds

  # Tool 실행마다 횟수, 경과 시간 검사
  def consume_tool_rounds(self):
    # 툴 사용 -> 라운드 1회 증가
    self.tool_rounds += 1
    # 체크
    self.check()

  # 현재 제약조건 검사
  def check(self):
    # 체크
    if self.tool_rounds > self.limits.max_tool_rounds:
      raise RuntimeError("툴 사용 제한 횟수 초과.")
    if time.monotonic() - self.started > self.limits.max_seconds:
      raise RuntimeError("실제 실행 시간 제한 초과.")
    print('하네스 체크 통과 (툴 실행 횟수, 툴 수행시간)')

  


# 요청한 툴이 허용한 툴 목록에 존재하는 지 확인
def assert_allowed_tool(name:str):
  # 에이전트 별로 제한적인 툴 범위 구성 가능
  if name not in ALLOWED_TOOLS:
    raise PermissionError(f"해당 툴 사용은 허용되지 않았습니다. {name}")
