# 목표
- 하네스 엔지니어링
  - 바이브 코딩
    - 코딩 에이전트가 코드를 안전하고 일관되게 하여 불필요한 작업을 줄이고 항상 기억할 내용 세팅 등을 반영하여 코드작성, 실행, 검증하도록 전체를 둘러싸고 있는 실행환경/규칙 전체를 의미
    - ex) claude.md
  - Agent의 Tool 실행
    - Agent가 동작할 수 있는 범위, 권한, 비용, 시간, 검증 규칙 등을 설계하는 것

# 비교
| 개념 | Coding Agent Harness | 현재 Agent Harness |
|---|---|---|
| 실행 대상 | 코드·Shell·파일·Git | Tool |
| 권한 통제 | 허용 명령/경로 | `ALLOWED_TOOLS` |
| 실행 제한 | timeout, 최대 반복 | `Budget` |
| 위험 작업 차단 | rm, 임의 shell 등 | `assert_allowed_tool()` |
| 검증 | test/lint/build | Tool 결과/Verifier |
| 목적 | 코딩 Agent 통제 | 업무 Agent 통제 |


# 구성
```
/
L app
    L harness.py                  : 정책 계층 구성
L steps
    L step20_harness_guardrail.py : 하네스 적용 에이전트 수행 테스트
```
