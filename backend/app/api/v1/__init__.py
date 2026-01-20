"""
Инициализация маршрутов API v1.
"""

from fastapi import APIRouter

from app.api.v1 import health, profiles, calculate

from fastapi import APIRouter


router = APIRouter()


# Подключаем роутеры из модулей
router.include_router(health.router)
router.include_router(profiles.router)
router.include_router(calculate.router)
# Здесь позже подключим calculate.router
