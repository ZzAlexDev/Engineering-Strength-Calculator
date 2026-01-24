import type {
    BeamCalculationRequest,
    BeamCalculationResponse,
    MaterialProfileList
} from '../types/calculator'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const calculatorService = {
    async calculate(data: BeamCalculationRequest): Promise<BeamCalculationResponse> {
        const response = await fetch(`${API_BASE_URL}/api/v1/calculate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })

        if (!response.ok) {
            const error = await response.json()
            throw new Error(error.detail || 'Calculation error')
        }

        return await response.json()
    },

    async getProfiles(): Promise<MaterialProfileList> {
        const response = await fetch(`${API_BASE_URL}/api/v1/profiles`)
        if (!response.ok) throw new Error('Failed to load profiles')
        return await response.json()
    }
}