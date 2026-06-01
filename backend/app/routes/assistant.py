from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.mistral_service import ask_mistral_question

router = APIRouter(tags=["assistant"])


class AssistantRequest(BaseModel):
    question: str


class AssistantResponse(BaseModel):
    answer: str


@router.post("/assistant", response_model=AssistantResponse)
async def ask_assistant(payload: AssistantRequest) -> AssistantResponse:
    try:
        answer = await ask_mistral_question(payload.question)
        return AssistantResponse(answer=answer)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
