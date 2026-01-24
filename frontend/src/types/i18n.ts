export type Locale = 'ru' | 'en'

export interface TranslationStructure {
    app: {
        title: string
        subtitle: string
        footer: string
    }
    beamInput: {
        length: string
        supportType: string
        force: string
        forcePosition: string
        forcePositionHint: string
        profile: string
        calculate: string
        loadingProfiles: string
        noProfiles: string
    }
    supportTypes: {
        hinged: string
        cantilever: string
        fixed: string
    }
    errors: {
        noProfile: string
        backendError: string
        emptyProfiles: string
        calculationFailed: string
    }
}

export type TranslationKey = string