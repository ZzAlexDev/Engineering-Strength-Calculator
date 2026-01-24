import { ref, computed } from 'vue'  // <-- Добавляем Vue реактивность
import type { Locale, TranslationStructure } from '../types/i18n'

// Импорты JSON
import ruTranslations from '../locales/ru.json'
import enTranslations from '../locales/en.json'

const translations: Record<Locale, TranslationStructure> = {
    ru: ruTranslations as TranslationStructure,
    en: enTranslations as TranslationStructure
}

class I18nService {
    // Делаем locale реактивным ref
    private locale = ref<Locale>('ru')

    constructor() {
        // Восстанавливаем из localStorage
        const savedLocale = localStorage.getItem('app-locale') as Locale
        if (savedLocale && translations[savedLocale]) {
            this.locale.value = savedLocale
        }
    }

    // Вычисляемое свойство для текущих переводов
    private currentTranslations = computed(() => translations[this.locale.value])

    // Методы теперь используют .value для реактивности
    setLocale(newLocale: Locale): void {
        if (translations[newLocale]) {
            this.locale.value = newLocale
            localStorage.setItem('app-locale', newLocale)
        }
    }

    getLocale(): Locale {
        return this.locale.value
    }

    t(key: string, params?: Record<string, string>): string {
        const keys = key.split('.')
        let value: any = this.currentTranslations.value

        for (const k of keys) {
            if (value && typeof value === 'object' && k in value) {
                value = value[k]
            } else {
                console.warn(`[i18n] Key not found: "${key}"`)
                return key
            }
        }

        let result = String(value)
        if (params && typeof result === 'string') {
            for (const [paramName, paramValue] of Object.entries(params)) {
                result = result.replace(new RegExp(`{${paramName}}`, 'g'), paramValue)
            }
        }

        return result
    }

    getSupportTypes(): Array<{ label: string; value: string }> {
        return [
            { label: this.t('supportTypes.hinged'), value: 'hinged' },
            { label: this.t('supportTypes.cantilever'), value: 'cantilever' },
            { label: this.t('supportTypes.fixed'), value: 'fixed' }
        ]
    }

    // Геттер для Vue, чтобы отслеживать изменения
    get currentLocale() {
        return this.locale
    }
}

export const i18n = new I18nService()
export default i18n