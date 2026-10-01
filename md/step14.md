# 목표
- Agent Memory
- PostgreSQL + pgvector 방식으로 지식 저장(현재) + Memory 저장소 활용
- Memory 저장소를 활용하면 짧은 답변, 기존 질문에 대한 답변을 메모리에서 체크하여 LLM 사용없이 응답 가능한 구조 구성 -> 중요도 관리 -> 토큰 비용(운영비) 절감 도움
- 장기기억 활용

- 역할
  - LLM : 판단, 답변을 담당하는 두뇌
  - RAG : 회사 문서, 규정 등 LLM이 모르는 정보
  - DB :  실제 데이터 저장 및 조회
  - Memory : 사용자의 맥락/패턴 기억 -> 사용자 지시, 답변형태, 업무방식, 기억 포인트 등 저장 -> 사용자 질문 시 해당 내용을 기반으로 답변할 때 활용
    - 사용자가 선호하는 방식으로 답변을 구성하도록 도움
    - LLM이 추론할 때, 사용자가 누구인지, 어떤 업무를 하는지, 어떤 방식으로 답변받기를 원하는지를 프롬프트에 삽입
    - 매번 처음 질의하는 것처럼 행동하지 않고 과거의 중요한 맥락(정보)을 제공하는 역할 담당

# 구조
```
/
L sql
    L 005_memory.sql      : 사용자의 정보를 저장하는 테이블
L app
    L tools
        L memory_tools.py : 맥락을 저장하는 메모리 역할
    L agent
        L graph.py        : Memory Tool 등록
    L config.py           : 사용자 ID 환경변수 구성
L steps
    L step14_memory.py    : Memory 테스트 용
L .env                    : 사용자 ID 더미 구성
```

# SQL 반영
```
python -m scripts.migrate
---
# 테이블 구조 확인
\d agent_memories
```

# 실행
```
python -m steps.step14_memory
----
id | user_id  |                       content                        
----+----------+------------------------------------------------------
  1 | de-ai-19 | 답변 형식 선호: 짧은 bullet 형태로 답변받기를 선호함
```

# 사용자 메모리 유도 테스트
```
---
TOOL CALLS :  ['refund_summary', 'search_company_policy', 'recall_user_memory']
📌 2026년 9월 1주차 환불 현황 (09/01~09/07)\n\n**환불 현황**\n- 환불 건수: 1건\n- 환불 금액: 99,000원\n- 환불 사유: 제품 불량(product_defect)
⚠️ 주의 포인트 (정책 기준: CS-REFUND-2026)**\n- 환불 금액 99,000원 → **5만원 이상 환불은 팀장 승인 필요**(사용자 업무 규칙) → 승인 이력 확인 필요
```