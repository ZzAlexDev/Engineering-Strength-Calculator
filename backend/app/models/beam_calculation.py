"""
Pydantic-схемы для расчёта балки.
Содержит модели запроса и ответа API.
"""
from typing import Literal, Dict, List, Optional
from pydantic import BaseModel, Field, confloat, conlist


class BeamCalculationRequest(BaseModel):
    """Модель запроса на расчёт балки."""
    
    length: confloat(gt=0) = Field(
        ...,
        description="Длина пролёта (L), м",
        example=5.0,
        gt=0
    )
    
    support_type: Literal["hinged", "cantilever", "fixed"] = Field(
        ...,
        description="Тип опор балки",
        example="hinged"
    )
    
    force: confloat(gt=0) = Field(
        ...,
        description="Величина сосредоточенной силы (F), кН",
        example=100.0,
        gt=0
    )
    
    force_position: confloat(ge=0, le=1) = Field(
        ...,
        description="Координата приложения силы (доля от длины, 0..1)",
        example=0.5,
        ge=0,
        le=1
    )
    
    profile_name: str = Field(
        ...,
        description="Наименование стального профиля",
        example="I-beam_20B1",
        min_length=1
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "length": 5.0,
                "support_type": "hinged",
                "force": 100.0,
                "force_position": 0.5,
                "profile_name": "I-beam_20B1"
            }
        }


class BeamCalculationResponse(BaseModel):
    """Модель ответа с результатами расчёта балки."""
    
    input_data: BeamCalculationRequest = Field(
        ...,
        description="Исходные данные расчёта"
    )
    
    reactions: Dict[str, float] = Field(
        ...,
        description="Реакции опор, кН",
        example={"R_a": 50.0, "R_b": 50.0}
    )
    
    max_moment: float = Field(
        ...,
        description="Максимальный изгибающий момент (M_max), кН·м",
        example=125.0
    )
    
    max_deflection: float = Field(
        ...,
        description="Максимальный прогиб (f_max), мм",
        example=12.5
    )
    
    max_stress: float = Field(
        ...,
        description="Максимальное нормальное напряжение (σ_max), МПа",
        example=150.0
    )
    
    is_strength_sufficient: bool = Field(
        ...,
        description="Вердикт по прочности",
        example=True
    )
    
    is_stiffness_sufficient: bool = Field(
        ...,
        description="Вердикт по жёсткости",
        example=True
    )
    
    profile_properties: Dict[str, float] = Field(
        ...,
        description="Геометрические характеристики профиля",
        example={
            "moment_of_inertia_ix_cm4": 1840.0,
            "moment_of_resistance_wx_cm3": 184.0
        }
    )
    
    report_sections: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Текстовые блоки для отчёта"
    )
    
    diagram_data: Dict[str, List[List[float]]] = Field(
        ...,
        description="Данные для построения эпюр",
        example={
            "moments": [[0.0, 0.0], [2.5, 125.0], [5.0, 0.0]],
            "positions": [[0.0, 0.0], [5.0, 0.0]]
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "input_data": {
                    "length": 5.0,
                    "support_type": "hinged",
                    "force": 100.0,
                    "force_position": 0.5,
                    "profile_name": "I-beam_20B1"
                },
                "reactions": {"R_a": 50.0, "R_b": 50.0},
                "max_moment": 125.0,
                "max_deflection": 12.5,
                "max_stress": 150.0,
                "is_strength_sufficient": True,
                "is_stiffness_sufficient": True,
                "profile_properties": {
                    "moment_of_inertia_ix_cm4": 1840.0,
                    "moment_of_resistance_wx_cm3": 184.0
                },
                "report_sections": [
                    {"title": "Исходные данные", "content": "Длина: 5.0 м"},
                    {"title": "Результаты", "content": "Момент: 125.0 кН·м"}
                ],
                "diagram_data": {
                    "moments": [[0.0, 0.0], [2.5, 125.0], [5.0, 0.0]],
                    "positions": [[0.0, 0.0], [5.0, 0.0]]
                }
            }
        }