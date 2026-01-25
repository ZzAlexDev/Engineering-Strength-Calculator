<template>
    <div class="app-container">
        <header class="app-header">
            <div class="logo">
                <h1>{{ i18n.t('app.title') }}</h1>
                <p>{{ i18n.t('app.subtitle') }}</p>
            </div>
            <LanguageSwitcher />
        </header>

        <main class="app-main">
            <BeamInputForm @calculate="handleCalculate" />
            
            <!-- ВРЕМЕННО: отображаем сырой JSON -->
            <div v-if="result" class="results">
                <h2>{{ i18n.t('results.title') }}</h2>
                <pre>{{ result }}</pre>
            </div>
        </main>

        <footer class="app-footer">
            <p>{{ i18n.t('app.footer') }}</p>
        </footer>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, provide } from 'vue'
import BeamInputForm from '@/components/BeamInputForm.vue'
import LanguageSwitcher from '@/components/LanguageSwitcher.vue'
import { calculatorService } from '@/services/calculatorService'
import { i18n } from '@/services/i18n.service'  // ← ТОЛЬКО ОДИН РАЗ импортируем!
import type { BeamCalculationResponse, BeamCalculationRequest } from '@/types/calculator'

// Реактивная локаль для дочерних компонентов
const locale = computed(() => i18n.getLocale())

// Результаты расчета
const result = ref<BeamCalculationResponse | null>(null)
    
// Обработчик расчета
const handleCalculate = async (data: BeamCalculationRequest) => {
    try {
        console.log('Отправка данных:', data)
        result.value = await calculatorService.calculate(data)
        console.log('Получены результаты:', result.value)
    } catch (error: any) {
        console.error('Ошибка расчета:', error)
        alert(i18n.t('errors.calculationFailed', { 
            message: error.message 
        }))
    }
}

// Пробрасываем i18n в дочерние компоненты через provide
provide('i18n', { 
    t: i18n.t.bind(i18n),
    locale,
    setLocale: i18n.setLocale.bind(i18n)
})
</script>

<style scoped>
.app-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

.app-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #e5e7eb;
}

.logo h1 {
    margin: 0;
    font-size: 1.5rem;
}

.logo p {
    margin: 0.25rem 0 0;
    color: #6b7280;
}

.app-main {
    min-height: 400px;
}

.results {
    margin-top: 2rem;
    padding: 1rem;
    background: #f9fafb;
    border-radius: 8px;
    font-family: monospace;
    white-space: pre-wrap;
    word-wrap: break-word;
}

.results h2 {
    margin-top: 0;
}

.app-footer {
    margin-top: 3rem;
    padding-top: 1rem;
    text-align: center;
    color: #6b7280;
    border-top: 1px solid #e5e7eb;
}
</style>