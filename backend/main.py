# backend/main.py

import sys
import os
sys.path.append(os.path.abspath(".."))  # Add root path


from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agent.langgraph_agent import run_agent  # 👈 make sure the import path is correct

app = FastAPI()

# Allow frontend (Streamlit) to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "TailorTalk backend is running."}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_msg = data.get("message", "")
    response = run_agent(user_msg)
    return {"response": response}
