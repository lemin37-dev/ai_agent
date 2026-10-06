# 목표
- Agent를 백엔드 서비스로 구성
  - fastapi 사용
    - dockerfile 구성
    - 소스코드 같이 구성하여 배포 (CI/CD X)
  - postgresql (임시 docker or RDS)
- Cloud에 배포
- 기존 코드 최대한 유지 -> 컨테이너 -> 인프라 자동화 -> 배포

# 구조
```
/
L app
    L main.py     : Agent를 fastapi에서 가급적 공용으로 실행하도록 함수 추가
    L service.py  : fastapi로 백엔드 구성, /chat, /health
L steps
    L step21_agent_service.py   : 로컬 fastapi 구동
--- 도커
L requirement.txt               : fastapi, unvicorn 추가
L dockerfile                    : Agent 구동 이미지
L docker-compose.yaml           : 수정, 2개 서비스(postgreSQL, Agent Service)
--- 인프라
L infra
    L scripts
        L bootstrap.sh|bat      : EC2(인프라) 자동 배포 구성
    L terraform
        L *.tf
```

# 로컬 실행
```
python -m steps.step21_agent_service
```

# Agent 컨테이너화
- Dockerfile 구성하여 이미지 생성
  - Fastapi + LangGraph 등

# Docker Compose
- 서비스
  - Agent 컨테이너 추가
- 컨테이너 구성
  ```
  docker compose up -d --build
  ```