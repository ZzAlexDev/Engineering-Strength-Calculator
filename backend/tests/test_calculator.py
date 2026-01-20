"""
Тесты для сервиса расчета балки.
"""
import sys
import os
import pytest

# Добавляем папку app в Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.calculator import BeamCalculator
from app.models.beam_calculation import BeamCalculationRequest
from app.models.material_profile import MaterialProfile


class TestBeamCalculator:
    """Тесты калькулятора балки."""
    
    def setup_method(self):
        """Настройка перед каждым тестом."""
        self.calculator = BeamCalculator()
        
        # Тестовый профиль (двутавр 20Б1)
        self.test_profile = MaterialProfile(
            name="Двутавр 20Б1",
            standard="ГОСТ 26020-83",
            key="I-beam_20B1",
            moment_of_inertia_ix_cm4=1840.0,
            moment_of_resistance_wx_cm3=184.0,
            height_mm=200.0,
            width_mm=100.0,
            mass_kg_m=22.7
        )
    
    def test_calculate_reactions_hinged_center(self):
        """Тест расчета реакций для шарнирно-опёртой балки с силой посередине."""
        # Сила 100 кН посередине балки 5 м
        reactions = self.calculator._calculate_reactions(
            length=5.0,
            force=100.0,
            force_position=0.5,
            support_type="hinged"
        )
        
        # Ожидаемые реакции: R_a = R_b = 50 кН
        assert reactions["R_a"] == 50.0
        assert reactions["R_b"] == 50.0
    
    def test_calculate_reactions_hinged_offset(self):
        """Тест расчета реакций для силы не по центру."""
        # Сила 100 кН на расстоянии 2 м от левой опоры (5 м балка)
        reactions = self.calculator._calculate_reactions(
            length=5.0,
            force=100.0,
            force_position=0.4,  # 2 м / 5 м = 0.4
            support_type="hinged"
        )
        
        # R_a = 100 * 3 / 5 = 60 кН, R_b = 100 * 2 / 5 = 40 кН
        assert reactions["R_a"] == 60.0
        assert reactions["R_b"] == 40.0
    
    def test_calculate_max_moment_hinged_center(self):
        """Тест расчета максимального момента для силы посередине."""
        max_moment = self.calculator._calculate_max_moment(
            length=5.0,
            force=100.0,
            force_position=0.5,
            support_type="hinged"
        )
        
        # M_max = (100 * 2.5 * 2.5) / 5 = 125 кН·м
        assert max_moment == 125.0
    
    def test_calculate_max_stress(self):
        """Тест расчета напряжения."""
        # Момент 125 кН·м, Wx = 184 см³
        stress = self.calculator._calculate_max_stress(
            max_moment=125.0,
            moment_of_resistance=184.0
        )
        
        # σ = M / W = (125000 Н·м) / (184e-6 м³) ≈ 679.35 МПа
        # Проверяем приблизительно
        assert 670 < stress < 690
    
    def test_check_strength_sufficient(self):
        """Тест проверки прочности (достаточная)."""
        # Допустимое 240 МПа, фактическое 200 МПа
        is_sufficient = self.calculator._check_strength(200.0)
        assert is_sufficient is True
    
    def test_check_strength_insufficient(self):
        """Тест проверки прочности (недостаточная)."""
        # Допустимое 240 МПа, фактическое 300 МПа
        is_sufficient = self.calculator._check_strength(300.0)
        assert is_sufficient is False
    
    def test_full_calculation(self):
        """Полный тест расчета."""
        request = BeamCalculationRequest(
            length=5.0,
            support_type="hinged",
            force=100.0,
            force_position=0.5,
            profile_name="I-beam_20B1"
        )
        
        result = self.calculator.calculate(request, self.test_profile)
        
        # Проверяем основные поля
        assert result.input_data == request
        assert result.reactions["R_a"] == 50.0
        assert result.reactions["R_b"] == 50.0
        assert result.max_moment == 125.0
        assert isinstance(result.max_stress, float)
        assert isinstance(result.is_strength_sufficient, bool)
        assert isinstance(result.is_stiffness_sufficient, bool)
        assert "report_sections" in result.model_dump()
        assert "diagram_data" in result.model_dump()
    
    def test_generate_report_sections(self):
        """Тест формирования отчета."""
        request = BeamCalculationRequest(
            length=5.0,
            support_type="hinged",
            force=100.0,
            force_position=0.5,
            profile_name="I-beam_20B1"
        )
        
        reactions = {"R_a": 50.0, "R_b": 50.0}
        sections = self.calculator._generate_report_sections(
            request=request,
            profile=self.test_profile,
            reactions=reactions,
            max_moment=125.0,
            max_deflection=12.5,
            max_stress=150.0,
            is_strength_sufficient=True,
            is_stiffness_sufficient=True
        )
        
        assert len(sections) == 4
        assert sections[0]["title"] == "Исходные данные"
        assert sections[1]["title"] == "Реакции опор"
        assert "Длина пролёта: 5.0 м" in sections[0]["content"]
        assert "R_a: 50.0 кН" in sections[1]["content"]