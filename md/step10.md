# 목표
- 문단 단위 청킹, 시멘틱 청킹
- 메타데이터 필터링
- 벡터 + 키워드 하이브리드 검색(추론 시 비율로 활용)

# 시멘틱 청킹
- 말뭉치 -> 분절(문장/문단단위) -> 단위 별 임베딩 -> 인접 유사도 계산(앞 뒤 벡터간 유사도 계산) -> 유사도가 특정 임계값보다 낮아지는 지점 체크(최소 기준필요)-> 청킹
- 유사도가 높은 문장/문단 간 청킹 진행
- 임계값의 최적화는 다른 문제 -> 차후 추론 등 과정을 통해서 평가 진행
- 임계값은 임시 설정
  - 변수 : 임베딩 모델, 문서(말뭉치 원소스)의 구성과 특성, 유사도 임계값, 사용(추론행위) -> 평가

# 구조
```
/
L app
    L retrieval.py    : 업그레이드
    L ingestion/
        L ingest.py   : 업그레이드
        L splitter.py : 업그레이드
L steps
    L step10_rag_advanced.py
    
```

# 실행
```
python -m steps.step10_rag_advanced
```

# 시멘틱 청킹 후 DB에 입력
- app.ingestion.ingest.py 수정
  - 청킹의 종류별로 사용할 수 있는 상위 함수 구성
  - 데이터를 구축하는 부분에 함수 대체
```
# 실행
python -m steps.step8_document_ingestion

# psql 접속 후 확인
select
  id, document_id, chunk_index,
  left(content, 10) || '...' as content,
  left(embedding::text, 10) || '...' as embedding,
  left(metadata::text, 10) || '...' as metadata
from
  document_chunks;
----
id | document_id | chunk_index |        content        |   embedding   |   metadata    
----+-------------+-------------+-----------------------+---------------+---------------
 58 |           1 |           0 | # 고객 반품 및 ...    | [-0.070660... | {"category...
 59 |           1 |           1 | 일반 반품은 상품 ...  | [-0.050497... | {"category...
 60 |           1 |           2 | 고객 과실로 상품이... | [-0.053973... | {"category...
 61 |           1 |           3 | 상품 자체의 제조상... | [-0.130974... | {"category...
 62 |           1 |           4 | 주문한 상품과 다른... | [-0.082948... | {"category...
 63 |           1 |           5 | 환불은 반품 상품이... | [-0.099278... | {"category...
 64 |           1 |           6 | 단순 변심에 의한 ...  | [-0.075332... | {"category...
 65 |           1 |           7 | 반품 상품에 사은품... | [-0.059442... | {"category...
 66 |           1 |           8 | 고객센터 담당자는 ... | [-0.055384... | {"category...
```
