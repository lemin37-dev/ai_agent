# 목표
- 문서 레벨로 DB에 데이터 삽입
- 문서(말뭉치) -> 쪼개는 과정 필요함(청킹, chunk 단위로 자름)
  - 단순 크기 -> ... -> sementic chunking (주제가 변경되면 자름)
  - RAG 서비스 -> 질문의 포인트는 청킹 기준을 어떻게 수행했는가?
  - 문서 테이블(1), 청킹 테이블(N)
  - 문서 (md + 텍스트형태 제공)
    - Markdown formatter 처리(메타데이터), document chunking 처리(임베딩처리)

# 데이터
- cs, sales, hr 관련 사내 규정 문서
- 현재 = 메타데이터 + 규정
- 향후 규정 내용을 더 확대 예정 (청킹이 n개로 확장되는 것 확인)

# 구조
```
L sql
  L migrations
    L 002_documents.sql
L steps
  L step8_document_ingestion.py
L app
  L ingestion
    L __init__.py
    L ingest.py
    L loader.py
    L splitter.py
```

# 데이터를 벡터화 디비 입력 절차
- 002_documents.sql 수행
- 테이블 생성
```
python -m scripts.migrate
```

# 실행
```
python -m steps.step8_document_ingestion
```

# 청킹종류
| 방식 | 기준 | 특징 | 적합한 경우 |
|---|---|---|---|
| **Fixed-size** | 글자/토큰 수 | 가장 단순 | 기본 실습 |
| **Recursive** | 문단 → 문장 → 글자 | 구조를 최대한 유지 | 일반 RAG ⭐ |
| **Sentence** | 문장 | 문장 단위 보존 | FAQ, 짧은 문서 |
| **Structure-based** | 제목/섹션/Markdown | 문서 구조 보존 | 사내 업무 문서 ⭐ |
| **Semantic** | 의미 유사도 | 의미가 바뀌는 지점에서 분리 | 고급 RAG ⭐ |
| **Parent-Child** | 큰 Chunk + 작은 Chunk | 검색과 답변 컨텍스트 분리 | 긴 문서 |
| **Agentic** | LLM/Agent 판단 | 문맥·주제에 따라 동적 분할 | 고급/Agentic RAG |

# 확인
```
select * from documents;
-----
id |    document_code    | department | category |         title          |           source           | version | effective_date |          created_at           
----+---------------------+------------+----------+------------------------+----------------------------+---------+----------------+-------------------------------
  1 | CS-REFUND-2026      | CS         | refund   | 고객 반품 및 환불 정책 | data\cs\refund_policy.md   | 2026.3  | 2026-04-01     | 2026-09-29 05:16:25.503082+00
  2 | HR-LEAVE-2026       | HR         | leave    | 연차휴가 운영 규정     | data\hr\leave_policy.md    | 2026.1  | 2026-01-01     | 2026-09-29 05:16:25.535005+00
  3 | HR-TRAVEL-2026      | HR         | travel   | 국내 출장비 규정       | data\hr\travel_policy.md   | 2026.2  | 2026-03-01     | 2026-09-29 05:16:25.579741+00
  4 | SALES-DISCOUNT-2026 | SALES      | discount | 기업 고객 할인 정책    | data\sales\sales_policy.md | 2026.1  | 2026-02-01     | 2026-09-29 05:16:25.603981+00
```

```
select
  id, document_id, chunk_index,
  left(content, 10) || '...' as content,
  left(embedding::text, 10) || '...' as embedding,
  left(metadata::text, 10) || '...' as metadata
from
  document_chunks;
-----
id | document_id | chunk_index |        content        |   embedding   |   metadata    
----+-------------+-------------+-----------------------+---------------+---------------
 36 |           2 |           0 | # 연차휴가 운영 ...   | [-0.071822... | {"category...
 37 |           2 |           1 | 휴가 신청은 원칙적... | [-0.040641... | {"category...
 38 |           2 |           2 | 질병, 가족의 긴급...  | [-0.034746... | {"category...
 39 |           2 |           3 | 연속 3영업일 이상...  | [-0.074118... | {"category...
 28 |           1 |           0 | # 고객 반품 및 ...    | [-0.055798... | {"category...
 29 |           1 |           1 | 고객 과실로 상품이... | [-0.053973... | {"category...
```