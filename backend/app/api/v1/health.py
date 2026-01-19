"""
Модуль эндпоинтов для проверки здоровья сервиса.
"""
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health():
    """Проверка здоровья API."""
    return {
        "status": "ok",
        "service": "engineering-strength-calculator",
        "version": "1.0.0"
    }