from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from .agent import Agent, AgentException


app = FastAPI()
internal_agent = Agent()


class Question(BaseModel):
    message: str


class Answer(BaseModel):
    message: str


class Message(BaseModel):
    message: str
    user_type: int


class Messages(BaseModel):
    messages: List[Message]


@app.post("/send_message")
def send_message(question: Question) -> Answer:
    try:
        res = internal_agent.get_response(message=question.message)
        return Answer(message=res)
    except AgentException as e:
        raise HTTPException(status_code=500, detail=e)


@app.post("/clear_chat_history")
def clear_chat_history():
    pass


@app.get("/get_chat_history")
def get_chat_history() -> Messages:
    pass
