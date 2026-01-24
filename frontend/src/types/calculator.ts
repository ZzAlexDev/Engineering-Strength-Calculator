export interface BeamCalculationRequest {
    length: number
    support_type: string
    force: number
    force_position: number
    profile_name: string
}

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

export interface MaterialProfile {
    name: string
    key: string
    standard: string
    moment_of_inertia_ix_cm4: number
    moment_of_resistance_wx_cm3: number
    height_mm: number
    width_mm: number
    mass_kg_m: number
}

export interface MaterialProfileList {
    profiles: MaterialProfile[]
}