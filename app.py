from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from utils.prompts import SYSTEM_PROMPT
from utils.retrieval import search_catalog
from utils.guardrails import is_off_topic
from utils.llm import generate_reply

app = FastAPI()


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    latest_user_message = ""

    for message in reversed(request.messages):
        if message.role == "user":
            latest_user_message = message.content
            break

    if is_off_topic(latest_user_message):
        return {
            "reply": "I can only help with SHL assessment recommendations.",
            "recommendations": [],
            "end_of_conversation": False
        }

    vague_queries = [
        "i need an assessment",
        "recommend a test",
        "help me hire",
        "assessment"
    ]

    if latest_user_message.lower() in vague_queries:
        return {
            "reply": "Could you share the role, seniority level, and key skills you are hiring for?",
            "recommendations": [],
            "end_of_conversation": False
        }

    recommendations = search_catalog(latest_user_message, top_k=5)

    reply = generate_reply(
        SYSTEM_PROMPT,
        [m.dict() for m in request.messages],
        recommendations
    )

    return {
        "reply": reply,
        "recommendations": recommendations,
        "end_of_conversation": True
    }
