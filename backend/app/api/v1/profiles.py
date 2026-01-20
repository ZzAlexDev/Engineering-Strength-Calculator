"""
API эндпоинты для работы с профилями материалов.
"""
from fastapi import APIRouter, Depends, HTTPException

from app.models.material_profile import MaterialProfile, MaterialProfileList
from app.core.dependencies import get_material_repository

router = APIRouter(tags=["profiles"])


@router.get("/profiles", response_model=MaterialProfileList)
async def get_all_profiles(
    repository = Depends(get_material_repository)
):
    """
    Получить все доступные стальные профили.
    
    Returns:
        Список всех профилей с геометрическими характеристиками
    """
    profiles = repository.get_all_profiles()
    return MaterialProfileList(profiles=profiles)


@router.get("/profiles/{profile_key}", response_model=MaterialProfile)
async def get_profile(
    profile_key: str,
    repository = Depends(get_material_repository)
):
    """
    Получить конкретный профиль по ключу.
    
    Args:
        profile_key: Уникальный ключ профиля (например, 'I-beam_20B1')
        
    Returns:
        Данные профиля
        
    Raises:
        HTTPException: 404 если профиль не найден
    """
    profile = repository.get_profile(profile_key)
    if not profile:
        raise HTTPException(
            status_code=404,
            detail=f"Профиль с ключом '{profile_key}' не найден"
        )
    return profile