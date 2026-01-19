"""
Инициализация маршрутов API v1.
"""
from fastapi import APIRouter

from app.api.v1 import health

router = APIRouter(prefix="/v1")

# Подключаем роутеры из модулей
router.include_router(health.router)
# Здесь позже подключим calculate.router