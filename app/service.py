'''
FastAPI 기반 Agent 서비스
'''
from fastapi import FastAPI
from pydantic import BaseModel
from app.main import invoke_agent

# Fastapi 객체 생성
app = FastAPI(title="에이전트 서비스", description="LangGraph + bedrock + Agent", version="1.0.0")

# 요청 시 데이터 구조
class ChatRequest(BaseModel):
  message:str

# 라우팅
# /chat
@app.post("/chat")
async def chat(req:ChatRequest):
  # 에이전트에 질문을 담아 요청
  result = await invoke_agent(req.message)
  # 응답 결과 중 구조화된 데이터 획득
  final = result.get('final')
  print(req.message, " => ", final)
  if final:
    return final.model_dump() # 객체 직렬화
    #응답 메세지 구성
  return {
    "answer"     : result['messages'][-1].content,
    "sources"    : [],
    "tools_used" : [],
    "confidence" : 0.0
  }

# /health
@app.get("/health")
async def health():
  return {"status":"ok"}
