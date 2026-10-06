'''
- 에이전트의 루프 구성(흐름)을 위한 구조 설계
- 플래너, 검증 추가
- 루프 메인
'''

from pydantic import BaseModel, Field
from app.llm import get_chat_model
from app.agent.graph import build_graph


# 1. Planner 출력 구조 : 업무를 검증 가능한 범위내에 질문으로 분해(n개의 프럼프트(혹은 문장, 업무) 구성)
class Plan(BaseModel):
    subquestions:list[str] = Field(min_length=1, max_length=4) # 1, 혹은 4는 설정값
    pass

# 2. Verifier 출력 구조 : 결과 통과 여부, 통과 못할 경우 -> 부족한 근거
class Verifier(BaseModel):
    passed:bool
    gaps:list[str] = Field(default_factory=list)
    pass

# 3. Agentic Loop 구성 : 계획 -> 실행 -> 검증 -> 부족하다는 피드백 나오면 재시도
#    시간/비용 고려, 최대 재시도 회수 설정(실제 주입, 배제 고민, 주입 -> 이후 Human 개입 고려)
async def run_agentic_loop(task:str, max_attempts:int=2):
    # 3-1. 모델, 플랜구조, 검증구조, 피드백 변수
    model    = get_chat_model()
    planner  = model.with_structured_output(Plan)       # 질문 => 하위 질문으로 분해
    verifier = model.with_structured_output(Verifier)   # 실행 결과의 근거, 충분성 검증
    feedback = ""

    # 3-2. 
    for attempt in range(1, max_attempts+1): # 현재 구성상 기본 2회 반복
        # 3-2-1. PLAN -> REPLAN (feedback을 반영)
        plan = await planner.ainvoke(f'업무 질문을 검증 가능한 하위 질문 1~4개로 분해하세요. task={task}\nfeedback={feedback}')
        print(f'\n +++ ATTEMPT {attempt} +++')
        print("[PLAN]" if attempt == 1 else "[REPLAN]")

		# 3-2-2. EXECUTE -> 서브 질문별로 진행
        answers = []
        for i,q in enumerate(plan.subquestions, 1):
            result = await build_graph().ainvoke({
				"messages":[("user", q)], 
                "rounds":0, 
                "final":None
                }, config={"recursion_limit":18})
            # 답변 체크
            final = result.get("final")
            # 구조화 실패처리
            answer = final.answer if final else result['messages'][-1].content
            # 대답모음
            answers.append(answer)
            print(f"Q{i} 실행완료")

        # 답변을 하나의 말뭉치로 구성
        final_answer = "\n".join(f"Q{i+1}: {q}\nA{i+1}: {a}" for i, (q, a) in enumerate(zip(plan.subquestions, answers)))

        # 3-2-3. Verify
        ver_dict = await verifier.ainvoke(f"원래 업무를 답하기에 충분한지 검증하세요. task={task}\n{final_answer}")
        print(f"\n[VERIFY] passed={ver_dict.passed}")

        # pass 여부에 따른 반환처리
        if ver_dict.passed:
            return final_answer

        # feedback 구성
        feedback = "; ".join(ver_dict.gaps)
        print("[FEEDBACK]")
        for gap in ver_dict.gaps:
            print(f"- {gap}")

    # 최종응답 (최대 2회까지 반복하고 이후는 무조건 반환)
    return final_answer


