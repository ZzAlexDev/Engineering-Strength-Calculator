"""
Зависимости (Dependency Injection) для приложения.
"""
from app.repositories.material_repository import MaterialRepository, MaterialRepositoryStub


def get_material_repository() -> MaterialRepository:
    """
    Фабрика для получения репозитория материалов.
    
    Returns:
        MaterialRepository: Экземпляр репозитория
    """
    # В MVP возвращаем заглушку
    # В будущем можно заменить на реализацию с БД
    return MaterialRepositoryStub()
