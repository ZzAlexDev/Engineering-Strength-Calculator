"""
Сервис расчета балки на прочность и жёсткость.
Ядро бизнес-логики приложения.
"""
from typing import Dict, List, Tuple
from math import pow

from app.models.beam_calculation import BeamCalculationRequest, BeamCalculationResponse
from app.models.material_profile import MaterialProfile
from app.core.config import settings


class BeamCalculator:
    """Калькулятор для расчёта стальной балки."""
    
    # Модуль упругости стали, МПа
    STEEL_ELASTIC_MODULUS: float = 2.1e11  # 210,000 МПа = 2.1 × 10¹¹ Па


    
    def __init__(self):
        """Инициализация калькулятора."""
        pass
    
    def calculate(self, request: BeamCalculationRequest, profile: MaterialProfile) -> BeamCalculationResponse:
        """
        Основной метод расчёта балки.
        
        Args:
            request: Параметры расчёта балки
            profile: Данные стального профиля
            
        Returns:
            Результаты расчёта
        """
        # 1. Расчёт реакций опор
        reactions = self._calculate_reactions(
            request.length, 
            request.force, 
            request.force_position,
            request.support_type
        )
        
        # 2. Расчёт максимального момента
        max_moment = self._calculate_max_moment(
            request.length,
            request.force,
            request.force_position,
            request.support_type
        )
        
        # 3. Расчёт максимального прогиба
        max_deflection = self._calculate_max_deflection(
            request.length,
            request.force,
            request.force_position,
            request.support_type,
            profile.moment_of_inertia_ix_cm4
        )
        
        # 4. Расчёт максимального напряжения
        max_stress = self._calculate_max_stress(
            max_moment,
            profile.moment_of_resistance_wx_cm3
        )
        
        # 5. Проверка по прочности и жёсткости
        is_strength_sufficient = self._check_strength(max_stress)
        is_stiffness_sufficient = self._check_stiffness(
            max_deflection,
            request.length
        )
        
        # 6. Формирование данных для эпюр
        diagram_data = self._generate_diagram_data(
            request.length,
            request.force,
            request.force_position,
            request.support_type
        )
        
        # 7. Формирование отчёта
        report_sections = self._generate_report_sections(
            request,
            profile,
            reactions,
            max_moment,
            max_deflection,
            max_stress,
            is_strength_sufficient,
            is_stiffness_sufficient
        )
        
        return BeamCalculationResponse(
            input_data=request,
            reactions=reactions,
            max_moment=max_moment,
            max_deflection=max_deflection,
            max_stress=max_stress,
            is_strength_sufficient=is_strength_sufficient,
            is_stiffness_sufficient=is_stiffness_sufficient,
            profile_properties={
                "moment_of_inertia_ix_cm4": profile.moment_of_inertia_ix_cm4,
                "moment_of_resistance_wx_cm3": profile.moment_of_resistance_wx_cm3,
                "height_mm": profile.height_mm,
                "width_mm": profile.width_mm,
                "mass_kg_m": profile.mass_kg_m
            },
            report_sections=report_sections,
            diagram_data=diagram_data
        )
    
    def _calculate_reactions(self, length: float, force: float, 
                           force_position: float, support_type: str) -> Dict[str, float]:
        """Расчёт реакций опор."""
        # Для шарнирно-опёртой балки
        if support_type == "hinged":
            a = force_position * length
            b = length - a
            
            R_a = force * b / length
            R_b = force * a / length
            
            return {"R_a": round(R_a, 2), "R_b": round(R_b, 2)}
        
        # Для консоли
        elif support_type == "cantilever":
            return {"R_a": round(force, 2), "M_a": round(force * force_position * length, 2)}
        
        # Для жёсткой заделки
        elif support_type == "fixed":
            a = force_position * length
            R_a = force
            M_a = force * a
            return {"R_a": round(R_a, 2), "M_a": round(M_a, 2)}
        
        return {"R_a": 0.0, "R_b": 0.0}
    
    def _calculate_max_moment(self, length: float, force: float,
                            force_position: float, support_type: str) -> float:
        """Расчёт максимального изгибающего момента."""
        a = force_position * length
        
        if support_type == "hinged":
            # Максимальный момент под силой
            M_max = force * a * (length - a) / length
            return round(M_max, 2)
        
        elif support_type == "cantilever":
            # Максимальный момент в заделке
            M_max = force * a
            return round(M_max, 2)
        
        elif support_type == "fixed":
            # Упрощённо - момент под силой
            M_max = force * a * (length - a) / length
            return round(M_max, 2)
        
        return 0.0
    
    def _calculate_max_deflection(self, length: float, force: float,
                                force_position: float, support_type: str,
                                moment_of_inertia: float) -> float:
        """Расчёт максимального прогиба."""
        if support_type != "hinged":
            # Для MVP считаем только шарнирно-опёртую балку
            return 0.0
        
        # Переводим момент инерции из см⁴ в м⁴
        Ix = moment_of_inertia * 1e-8  # 1 см⁴ = 1e-8 м⁴
        
        # Переводим силу из кН в Н
        P = force * 1000  # кН → Н
        
        a = force_position * length
        b = length - a
        
        # Проверяем, находится ли сила посередине (с небольшой погрешностью)
        if abs(a - b) < 1e-6:  # a примерно равно b
            # Формула для силы посередине: f_max = (P * L³) / (48 * E * I)
            f_max_m = (P * length ** 3) / (48 * self.STEEL_ELASTIC_MODULUS * Ix)
        else:
            # Формула для силы не по центру: f_max = (P * a² * b²) / (3 * E * I * L)
            f_max_m = (P * a ** 2 * b ** 2) / (3 * self.STEEL_ELASTIC_MODULUS * Ix * length)
        
        # Переводим в миллиметры
        f_max_mm = f_max_m * 1000
        
        return round(f_max_mm, 3)


    def _calculate_max_stress(self, max_moment: float, 
                            moment_of_resistance: float) -> float:
        """Расчёт максимального нормального напряжения."""
        # Переводим момент сопротивления из см³ в м³
        Wx = moment_of_resistance * 1e-6  # см³ → м³
        
        # Переводим момент из кН·м в Н·м
        M = max_moment * 1000  # кН·м → Н·м
        
        # Напряжение σ = M / W
        stress = M / Wx  # Па
        stress_mpa = stress / 1e6  # Па → МПа
        
        return round(stress_mpa, 2)
    
    def _check_strength(self, max_stress: float) -> bool:
        """Проверка по прочности."""
        return max_stress <= settings.ALLOWABLE_STRESS
    
    def _check_stiffness(self, max_deflection: float, length: float) -> bool:
        """Проверка по жёсткости."""
        allowable_deflection = length * 1000 * settings.ALLOWABLE_DEFLECTION_RATIO  # мм
        return max_deflection <= allowable_deflection
    
    def _generate_diagram_data(self, length: float, force: float,
                             force_position: float, support_type: str) -> Dict[str, List[List[float]]]:
        """Генерация данных для построения эпюр."""
        # Упрощённые данные для MVP
        # В post-MVP сделаем точный расчёт точек
        
        a = force_position * length
        
        if support_type == "hinged":
            moments = [
                [0.0, 0.0],
                [a, force * a * (length - a) / length],
                [length, 0.0]
            ]
        else:
            moments = [[0.0, 0.0], [length, 0.0]]
        
        positions = [[0.0, 0.0], [length, 0.0]]
        
        return {
            "moments": moments,
            "positions": positions
        }
    
    def _generate_report_sections(self, request: BeamCalculationRequest,
                                profile: MaterialProfile, reactions: Dict[str, float],
                                max_moment: float, max_deflection: float,
                                max_stress: float, is_strength_sufficient: bool,
                                is_stiffness_sufficient: bool) -> List[Dict[str, str]]:
        """Формирование текстовых блоков отчёта."""
        # Словарь для перевода типов опор
        support_type_translation = {
            "hinged": "шарнирно-опёртая",
            "cantilever": "консоль",
            "fixed": "жёсткая заделка"
        }
        support_type_ru = support_type_translation.get(request.support_type, request.support_type)
        
        sections = [
            {
                "title": "Исходные данные",
                "content": f"Длина пролёта: {request.length} м\n"
                        f"Тип опор: {support_type_ru}\n"  # <-- ИСПРАВЛЕНО
                        f"Сила: {request.force} кН\n"
                        f"Положение силы: {request.force_position * 100}% длины\n"
                        f"Профиль: {profile.name}"
            },
            {
                "title": "Реакции опор",
                "content": "\n".join([f"{key}: {value} кН" for key, value in reactions.items()])
            },
            {
                "title": "Результаты расчёта",
                "content": f"Максимальный момент: {max_moment} кН·м\n"
                        f"Максимальный прогиб: {max_deflection} мм\n"
                        f"Максимальное напряжение: {max_stress} МПа"
            },
            {
                "title": "Проверка по нормам",
                "content": f"Прочность: {'✅ обеспечена' if is_strength_sufficient else '❌ не обеспечена'}\n"
                        f"Допустимое напряжение: {settings.ALLOWABLE_STRESS} МПа\n"
                        f"Жёсткость: {'✅ обеспечена' if is_stiffness_sufficient else '❌ не обеспечена'}\n"
                        f"Допустимый прогиб: L/{int(1/settings.ALLOWABLE_DEFLECTION_RATIO)}"
            }
        ]
        
        return sections
