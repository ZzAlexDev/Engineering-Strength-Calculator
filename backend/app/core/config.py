"""
Модуль конфигурации приложения.
Все настройки выносятся сюда, а не хардкодятся.
"""
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения."""
    
    # Базовые настройки
    APP_NAME: str = "Engineering Strength Calculator"
    ENV: str = "development"
    DEBUG: bool = True
    
    # CORS настройки
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173",
    ]
    
    # Настройки допустимых значений (заглушка для MVP)
    ALLOWABLE_STRESS: float = 240.0  # МПа, сталь С245
    ALLOWABLE_DEFLECTION_RATIO: float = 1/250  # L/250
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()