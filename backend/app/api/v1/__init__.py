"""
Инициализация маршрутов API v1.
"""

from fastapi import APIRouter

from app.api.v1 import health, profiles

from fastapi import APIRouter


router = APIRouter()


# Подключаем роутеры из модулей
router.include_router(profiles.router)

# Подключаем роутеры из модулей
router.include_router(health.router)
# Здесь позже подключим calculate.router
