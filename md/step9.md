# 목표
- RAG(Retrieval-Augmented Genration)
  - 검색증강, LLM이 학습하지 않는 LLM 기준 외부 데이터(사내데이터 등)를 검색을 통해 정보를 제공받아 기존 프롬프트와 결합하여 LLM에게 추론 처리
  - 검색은 벡터를 기반으로 진행 -> 데이터는 벡터화되어 벡터디비에 저장되어 있어야 함
  - LLM이 답변하기 전에 외부 지식에서 필요한 정보를 검색(Retrieval)하고, 그 정보를 근거로 답변(Genration)하도록 하는 방식
- Agent의 관점에서는 RAG는 Tool임
  - 도구 사용 여부
    - 규칙적 구성
    - 자율적으로 판단하게 구성
      - 정책 부여 : 사내 규정, 업무 지식 등의 질문은 RAG를 사용하도록 하는 등의 정책 부여
- RAG 기본 사용

# 구조
```
L app
  L retrieval.py       : 벡터 디비에 검색 후 결과 반환 함수 제공
  L rag.py             : 질문 -> 벡터디비 검색 -> 결과 + 프롬프트 -> LLM 추론요청 -> 응답
L steps
  L step9_rag_basic.py : 검색 증강 테스트용
```

# 실행
```
python -m steps.step9_rag_basic
```