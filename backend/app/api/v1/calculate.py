"""
API эндпоинты для расчёта балки.
"""
from fastapi import APIRouter, Depends, HTTPException

from app.models.beam_calculation import BeamCalculationRequest, BeamCalculationResponse
from app.services.calculator import BeamCalculator
from app.core.dependencies import get_material_repository

router = APIRouter(tags=["calculation"])
calculator = BeamCalculator()


@router.post("/calculate", response_model=BeamCalculationResponse)
async def calculate_beam(
    request: BeamCalculationRequest,
    repository = Depends(get_material_repository)
):
    """
    Расчёт балки на прочность и жёсткость.
    
    Args:
        request: Параметры расчёта балки
        
    Returns:
        Результаты расчёта с подробным отчётом
        
    Raises:
        HTTPException: 404 если профиль не найден
        HTTPException: 400 если данные некорректны
    """
    try:
        # Получаем профиль по имени
        profile = repository.get_profile(request.profile_name)
        if not profile:
            raise HTTPException(
                status_code=404,
                detail=f"Профиль '{request.profile_name}' не найден. "
                       f"Используйте GET /profiles для списка доступных."
            )
        
        # Выполняем расчёт
        result = calculator.calculate(request, profile)
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Логируем внутренние ошибки
        raise HTTPException(
            status_code=500,
            detail=f"Внутренняя ошибка сервера: {str(e)}"
        )