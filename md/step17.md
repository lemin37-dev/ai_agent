# 목표
- 검색 품질을 모호하게 판단하지 않고 반복 측정이 가능한 평가 데이터셋을 구성
- 질문, 답변 데이터 구성, 필요 시 반복 수행
  - 질의 -> 결과 -> 해석 및 평가
  - 평가지표는 Mean Reciprocal Rnak(MRR, 평균 역순위)
  - RAG 검색 정확도 평가

# 구조
```
/
L app
    L evaluation
        L __init__.py
        L dataset.py          : 테스트용 데이터 셋
        L retrieval_eval.py   : 평가
L steps
    L step17_evaluation.py    : 테스트 메인코드
```

# 실행
```
python -m steps.step17_evaluation
---
상품 자체 하자는 언제까지 환불할 수 있을까? -> ['CS-REFUND-2026', 'CS-REFUND-2026', 'CS-REFUND-2026', 'CS-REFUND-2026', 'CS-REFUND-2026'] | expected=CS-REFUND-2026 | rank=1

출장시 숙박비 한도는 얼마지? -> ['HR-TRAVEL-2026', 'HR-TRAVEL-2026', 'HR-TRAVEL-2026', 'HR-TRAVEL-2026', 'HR-TRAVEL-2026'] | expected=HR-TRAVEL-2026 | rank=1

1000만원 이상 추가 할인시 승인은 누가 하지? -> ['SALES-DISCOUNT-2026', 'SALES-DISCOUNT-2026', 'SALES-DISCOUNT-2026', 'SALES-DISCOUNT-2026', 'HR-LEAVE-2026'] | expected=SALES-DISCOUNT-2026 | rank=1

HitRate@5 = 1.000
MRR = 1.000
```

# 평가

| 지표 | 의미 | 핵심 질문 |
|---|---|---|
| **HitRate@K** | Top-K 안에 정답 문서가 하나라도 있는 비율 | 정답을 찾았나? |
| **MRR** | 첫 번째 정답 문서의 역순위 평균 | 정답이 얼마나 앞에 있나? |
| **Precision@K** | Top-K 중 실제 관련 문서의 비율 | 찾은 것 중 쓸모있는 게 얼마나 되나? |
| **Recall@K** | 전체 관련 문서 중 Top-K가 찾아낸 비율 | 필요한 문서를 얼마나 놓치지 않았나? |
| **NDCG@K** | 관련도가 높은 문서가 상위에 배치됐는지 평가 | 좋은 문서가 제대로 위에 있나? |
| **MAP** | 여러 관련 문서의 검색 순위를 종합 평가 | 관련 문서들을 전반적으로 잘 정렬했나? |

# 평가의 단계
```
1단계
HitRate@K
MRR
   ↓
검색 성공 + 검색 순위 평가

2단계
Precision@K
Recall@K
   ↓
검색 품질을 좀 더 세밀하게 평가

3단계
Faithfulness
Answer Relevance
   ↓
최종 생성 답변까지 평가

4단계
Latency / Token / Cost
   ↓
실제 Agent 운영 품질 평가
```