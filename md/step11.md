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