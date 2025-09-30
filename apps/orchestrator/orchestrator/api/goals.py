
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import BaseModel, Field
import uuid
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/goals",
    tags=["Goals"],
)

class GoalContext(BaseModel):
    message: str

class GoalPayload(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    context: GoalContext

@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def submit_goal(payload: GoalPayload = Body(...)):
    """
    Принимает новую цель для обработки.
    """
    logger.info(f"Received new goal with ID: {payload.id}, Name: {payload.name}")
    # Здесь будет логика для отправки цели в NATS или другую систему.
    # Пока просто логируем и возвращаем успешный ответ.
    return {"message": "Goal accepted for processing", "goal_id": payload.id}
