# 목표
- 운영상의 세밀한 평가 및 LangChain, LangGraph 운영 모니터링 등 추적하기 위한 장치 필요
  - LangSmith 설정

# 세팅
- LangSmith 가입
  - https://smith.langchain.com/
  - 대시보드 > 앱선택 > tracing -> project 생성 > key 생성 >.env copy

# 구조
```
/
L app
    L observability.py          : LangSmith 상태 반환
L steps
    L step18_observability.py
L .env                          : LangSmith 환경변수 추가
```

# 실행
```
python -m steps.step18_observability
```