/**
 * Типы данных для расчёта балки.
 * Соответствуют backend моделям (Pydantic схемам).
 */

// Запрос на расчёт балки
export interface BeamCalculationRequest {
    length: number           // Длина пролёта, м
    support_type: string     // Тип опор: 'hinged' | 'cantilever' | 'fixed'
    force: number            // Сила, кН
    force_position: number   // Положение силы (0..1)
    profile_name: string     // Ключ профиля
}

// Ответ с результатами расчёта
export interface BeamCalculationResponse {
    input_data: BeamCalculationRequest
    reactions: Record<string, number>
    max_moment: number
    max_deflection: number
    max_stress: number
    is_strength_sufficient: boolean
    is_stiffness_sufficient: boolean
    profile_properties: Record<string, number>
    report_sections: Array<{
        title: string
        content: string
    }>
    diagram_data: {
        moments: Array<[number, number]>
        positions: Array<[number, number]>
    }
}

// Модель стального профиля
export interface MaterialProfile {
    name: string                    // Наименование
    key: string                     // Уникальный ключ
    standard: string                // Стандарт (ГОСТ)
    moment_of_inertia_ix_cm4: number // Момент инерции
    moment_of_resistance_wx_cm3: number // Момент сопротивления
    height_mm: number               // Высота, мм
    width_mm: number                // Ширина, мм
    mass_kg_m: number               // Масса, кг/м
}

// Список профилей
export interface MaterialProfileList {
    profiles: MaterialProfile[]
}