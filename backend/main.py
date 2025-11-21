import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from generate import search_similar_chunks, generate_answer

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

@app.get("/")
def home():
    return {"status": "FastAPI backend running ✔"}

@app.post("/chat")
def chat(req: ChatRequest):
    user_prompt = req.query
    context = search_similar_chunks(user_prompt)
    answer = generate_answer(context, user_prompt)
    return {"answer": answer}