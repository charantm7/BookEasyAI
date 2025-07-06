from fastapi import APIRouter, Request
from backend.services.agent import get_prompt
from pydantic import BaseModel

router = APIRouter()

class Message(BaseModel):
    message: str

@router.post("/chat")
async def chat_endpoint(request:Message):
    data = request.message
    response = get_prompt(data)
    
    return {"reply":response}