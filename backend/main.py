from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agent.langgraph_agent import run_agent  # Adjust if needed

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_msg = data.get("message", "")
    response = run_agent(user_msg)
    return {"response": response}
