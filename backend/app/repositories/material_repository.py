from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.material_profile import MaterialProfile


class MaterialRepository(ABC):
    """Абстрактный класс репозитория материалов."""
    
    @abstractmethod
    def get_profile(self, profile_key: str) -> Optional[MaterialProfile]:
        """
        Получить профиль по ключу.
        
        Args:
            profile_key: Уникальный ключ профиля (например, 'I-beam_20B1')
            
        Returns:
            MaterialProfile или None если не найден
        """
        pass
    
    @abstractmethod
    def get_all_profiles(self) -> List[MaterialProfile]:
        """
        Получить все доступные профили.
        
        Returns:
            Список всех профилей
        """
        pass
    
    @abstractmethod
    def search_profiles(self, name_part: str) -> List[MaterialProfile]:
        """
        Поиск профилей по части названия.
        
        Args:
            name_part: Часть названия профиля
            
        Returns:
            Список подходящих профилей
        """
        pass


class MaterialRepositoryStub(MaterialRepository):
    """
    Заглушка репозитория материалов для MVP.
    Хранит данные в памяти.
    """
    
    def __init__(self):
        """Инициализация с тестовыми данными ГОСТ профилей."""
        self._profiles: dict[str, MaterialProfile] = {}
        self._initialize_data()
    
    def _initialize_data(self):
        """Инициализация тестовых данных."""
        profiles_data = [
            {
                "name": "Двутавр 10Б1",
                "standard": "ГОСТ 26020-83",
                "key": "I-beam_10B1",
                "moment_of_inertia_ix_cm4": 198.0,
                "moment_of_resistance_wx_cm3": 39.7,
                "height_mm": 100.0,
                "width_mm": 55.0,
                "mass_kg_m": 8.1
            },
            {
                "name": "Двутавр 14Б1",
                "standard": "ГОСТ 26020-83",
                "key": "I-beam_14B1",
                "moment_of_inertia_ix_cm4": 572.0,
                "moment_of_resistance_wx_cm3": 81.7,
                "height_mm": 140.0,
                "width_mm": 73.0,
                "mass_kg_m": 12.3
            },
            {
                "name": "Двутавр 20Б1",
                "standard": "ГОСТ 26020-83",
                "key": "I-beam_20B1",
                "moment_of_inertia_ix_cm4": 1840.0,
                "moment_of_resistance_wx_cm3": 184.0,
                "height_mm": 200.0,
                "width_mm": 100.0,
                "mass_kg_m": 22.7
            },
            {
                "name": "Двутавр 30Б1",
                "standard": "ГОСТ 26020-83",
                "key": "I-beam_30B1",
                "moment_of_inertia_ix_cm4": 6320.0,
                "moment_of_resistance_wx_cm3": 422.0,
                "height_mm": 300.0,
                "width_mm": 140.0,
                "mass_kg_m": 39.2
            },
            {
                "name": "Двутавр 40Б1",
                "standard": "ГОСТ 26020-83",
                "key": "I-beam_40B1",
                "moment_of_inertia_ix_cm4": 15760.0,
                "moment_of_resistance_wx_cm3": 788.0,
                "height_mm": 400.0,
                "width_mm": 155.0,
                "mass_kg_m": 57.0
            },
            {
                "name": "Двутавр 50Б1",
                "standard": "ГОСТ 26020-83",
                "key": "I-beam_50B1",
                "moment_of_inertia_ix_cm4": 39727.0,
                "moment_of_resistance_wx_cm3": 1589.0,
                "height_mm": 500.0,
                "width_mm": 180.0,
                "mass_kg_m": 89.8
            },
            {
                "name": "Двутавр 60Б1",
                "standard": "ГОСТ 26020-83",
                "key": "I-beam_60B1",
                "moment_of_inertia_ix_cm4": 76806.0,
                "moment_of_resistance_wx_cm3": 2560.0,
                "height_mm": 600.0,
                "width_mm": 190.0,
                "mass_kg_m": 108.0
            }
        ]
        
        for data in profiles_data:
            profile = MaterialProfile(**data)
            self._profiles[profile.key] = profile
    
    def get_profile(self, profile_key: str) -> Optional[MaterialProfile]:
        """Получить профиль по ключу."""
        return self._profiles.get(profile_key)
    
    def get_all_profiles(self) -> List[MaterialProfile]:
        """Получить все доступные профили."""
        return list(self._profiles.values())
    
    def search_profiles(self, name_part: str) -> List[MaterialProfile]:
        """Поиск профилей по части названия."""
        name_part_lower = name_part.lower()
        return [
            profile for profile in self._profiles.values()
            if name_part_lower in profile.name.lower()
        ]
