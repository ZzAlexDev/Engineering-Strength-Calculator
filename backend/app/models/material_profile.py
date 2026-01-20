"""
Pydantic-схемы для стальных профилей.
"""
from pydantic import BaseModel, Field


class MaterialProfile(BaseModel):
    """Модель стального профиля (двутавр)."""
    
    name: str = Field(
        ...,
        description="Наименование профиля",
        example="Двутавр 20Б1"
    )
    
    standard: str = Field(
        ...,
        description="Стандарт (ГОСТ)",
        example="ГОСТ 26020-83"
    )
    
    key: str = Field(
        ...,
        description="Уникальный ключ профиля",
        example="I-beam_20B1"
    )
    
    moment_of_inertia_ix_cm4: float = Field(
        ...,
        description="Момент инерции Ix, см⁴",
        example=1840.0,
        gt=0
    )
    
    moment_of_resistance_wx_cm3: float = Field(
        ...,
        description="Момент сопротивления Wx, см³",
        example=184.0,
        gt=0
    )
    
    height_mm: float = Field(
        ...,
        description="Высота профиля, мм",
        example=200.0,
        gt=0
    )
    
    width_mm: float = Field(
        ...,
        description="Ширина полки, мм",
        example=100.0,
        gt=0
    )
    
    mass_kg_m: float = Field(
        ...,
        description="Масса 1 м, кг",
        example=22.7,
        gt=0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Двутавр 20Б1",
                "standard": "ГОСТ 26020-83",
                "key": "I-beam_20B1",
                "moment_of_inertia_ix_cm4": 1840.0,
                "moment_of_resistance_wx_cm3": 184.0,
                "height_mm": 200.0,
                "width_mm": 100.0,
                "mass_kg_m": 22.7
            }
        }


class MaterialProfileList(BaseModel):
    """Модель списка профилей."""
    
    profiles: list[MaterialProfile] = Field(
        ...,
        description="Список доступных профилей"
    )