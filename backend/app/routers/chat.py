from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag_service import chat

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    response: str
    sources: list[str]


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        result = chat(request.session_id, request.message)
        return ChatResponse(
            response=result["response"],
            sources=result["sources"],
        )
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")
