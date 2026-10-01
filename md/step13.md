# 목표
- LangGraph + 정형데이터(postgresql) + 비정형데이터(pgvector) 추론
- 환불 통계(SQL Tool)와 환불 정책(RAG Tool)을 한 질문에서 함께 처리

# SQL
- 환불 통계를 위한 SQL 처리
```
python -m scripts.migrate
---
refund_id | order_id |      requested_at      |     reason     |  amount  |  status  
-----------+----------+------------------------+----------------+----------+----------
         1 |        8 | 2026-09-04 09:00:00+00 | product_defect | 99000.00 | approved
(1 row)
```

# 구조
```
/
L app
    L agent
        L graph.py            : 환불 통계 도구 등록
    L tools
        L sql_tools.py        : 환불 관련 함수(도구) 추가
L steps
    L step13_sql_rag_agent.py : 사용자 질문 처리
```

# 실행
```
python -m steps.step13_sql_rag_agent.py
---
## 1. 2026-09-01 ~ 2026-09-05 환불 현황

현재 제공된 조회 도구는 **`sales_summary`**(결제완료 매출·주문건수)와 **`top_products`**(결제완료 매출 기준 상위 제품)로, 둘 다 "결제 완료" 데이터만 집계하며 **환불/반품 건수나 환불 금액을 조회할 수 있는 도구는 제공되어 있지 않습니다.**
```

# 도구 추가 후 재실행
```
## 📊 환불 현황 (2026-09-01 ~ 2026-09-05)

| 항목 | 내용 |
|---|---|
| 환불 건수 | 1건 |
| 환불 금액 | 99,000원 |
| 환불 사유 | 상품 하자 (product_defect) |

해당 기간에는 **상품 하자로 인한 환불 1건**만 발생했습니다.
```