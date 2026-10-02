'''
- RAG 검색 정확도 평가용 테스트 케이스
- 각 질문에 대해 기대하는 문서가 검색되는지 검증
'''
CASES = [
  {
    "question":"상품 자체 하자는 언제까지 환불할 수 있을까?",
    "expected_source":"CS-REFUND-2026"
  },
  {
    "question":"출장 시 숙박비 한도는 얼마지?",
    "expected_source":"HR-TRAVEL-2026"
  },
  {
    "question":"1000만원 이상 추가 할인 시 승인은 누가 하지?",
    "expected_source":"SALES-DISCOUNT-2026"
  },
    
]