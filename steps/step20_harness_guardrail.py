'''
- 하네스를 적용하여 에이전트 작동시키는 테스트 코드
'''

# 기능 확인
from app.harness import ALLOWED_TOOLS, Budget, assert_allowed_tool

# Budget 생성
b = Budget()
b.consume_tool_rounds()
print("Round, Time 체크")
