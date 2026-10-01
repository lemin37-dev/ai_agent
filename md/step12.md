# 목표
- LangGraph + bedrock + LangChain + tools
- LangGraph
  - StateGraph -> Agent -> ToolNode -> Agent 순환루프를 구성하는 자율형 에이전트 기본 구성
  - Reason/Tool/Observe 루프 구성
- 질의 -> 적절한 Tool을 LLM이 선택하고 Tool 사용, 결과를 이용하여 관찰 -> 최종 답변까지 반복진행
- LangGraph 관점에서
  - 노드 : ToolNode, AgentNode 등 존재
  - 순서, 방향성 지정
    - 시작점 지정
    - 'A 노드에서 반드시 B 노드로 간다'와 같은 경로를 지정
    - 끝점 지정
  - 끝 노드의 출력값 -> 최종 추론 결과
  - 노드를 순환하면서 다양한 노드 사용 -> 흔적이 남음 -> MessagesState를 상속받은 객체에 저장
    - MessagesState는 messages(list) 변수에 순서대로 기록함
    - 통상 MessagesState를 상속받아 커스텀 변수를 추가해서 노드 상 State 관리를 수행

# 구조
```
/
L app
    L agent
        L __init__.py
        L graph.py      : LangGraph 구성 (노드 추가 등 구성)
        L prompts.py    : 에이전트의 프롬프트
        L state.py      : 상태관리
    L main.py           : 에이전트 구동
L steps
    L step12_langgraph_agent.py
```

# 실행
```
python -m steps.step12_langgraph_agent
```

# 판단 흐름
```
result["messages"]

[0] HumanMessage
    └─ 사용자 질문

[1] AIMessage
    └─ Tool Calls
    └─ search_company_policy

[2] ToolMessage
    └─ search_company_policy 결과
    
[4] AIMessage
    └─ 최종 답변

rounds = 2 (LLM 두번 추론)
```