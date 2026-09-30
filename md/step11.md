# 목표
- langchain tool 구성
- SQL 수행 tool, RAG tool, ..., 향후 외부도구 연결(MCP - 노션, 슬랙, 카톡 등)
- 도구 구성을 통해 에이전트가 자율적으로 판단하여 도구를 사용하도록 구성 -> lang graph

# 구조
```
/
L app
    L tools
        L __init__.py
        L rag_tools.py    : RAG을 도구로 사용할 수 있는 내용 적재 -> @tool
        L sql_tools.py    : SQL을 도구로 사용할 수 있는 내용 적재 -> @tool
L steps
    L step11_tools.py     : 툴 사용 테스트 코드
L sql
    L migration
        L 003_business.sql: sql 툴을 위한 대상 테이블과 더미 데이터
```

# 테이블 생성 및 데이터 삽입
```
python -m scripts.migrate
```

# 실행
```
python -m steps.step11_tools
---
# ----------------------------------
# sql_tools.sales_summary
# ----------------------------------
revenue=3586000.00, orders=8, range2026-09-01~2026-09-05

# ----------------------------------
# sql_tools.top_products
# ----------------------------------
1. 사내 AI Agent 구축:qty=1, revenue=1200000.00
2. RAG 구축 컨설팅:qty=1, revenue=800000.00
3. 데이터 분석 패키지:qty=4, revenue=600000.00

# ----------------------------------
# rag_tools.search_company_policy
# ----------------------------------
[source=HR-LEAVE-2026 | hybrid=0.382]
# 연차휴가 운영 규정

연차휴가는 직원의 휴식과 업무 지속 가능성을 보장하기 위한 제도이며, 직원은 부여된 휴가 범위에서 연차를 신청할 수 있다. 입사 1년 미만 직원은 근로한 기간과 사내 운영 기준에 따라 현재 사용할 수 있는 휴가일수를 인사 시스템에서 확인한 후 신청한다.
```
