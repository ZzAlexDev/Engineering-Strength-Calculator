"""
Основной модуль FastAPI приложения.
Здесь создается и настраивается экземпляр приложения.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import router as api_v1_router
from app.core.config import settings


def create_application() -> FastAPI:
    """Фабрика для создания экземпляра FastAPI приложения."""
    application = FastAPI(
        title="Engineering Strength Calculator API",
        description="API для расчёта прочности и жёсткости стальных балок",
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )
    
    # Настраиваем CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Подключаем маршруты API
    application.include_router(api_v1_router, prefix="/api/v1")
    
    return application


app = create_application()


@app.get("/")
async def root():
    """Корневой эндпоинт для проверки работы API."""
    return {
        "message": "Engineering Strength Calculator API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "health": "/api/v1/health"
    }


@app.get("/health")
async def health_check():
    """Эндпоинт для проверки здоровья сервиса."""
    return {"status": "healthy"}