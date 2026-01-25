<template>
    <div class="beam-input-form">
        <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
        </div>
        
        <form @submit.prevent="handleSubmit">
            <!-- 1. Поле ДЛИНА БАЛКИ -->
            <div class="field">
                <label for="length">{{ i18n.t('beamInput.length') }}</label>
                <InputNumber 
                    v-model="formData.length" 
                    id="length"
                    :min="0.1" 
                    :max="50" 
                    :step="0.1"
                    :useGrouping="false"
                    mode="decimal"
                    :minFractionDigits="1"
                    :maxFractionDigits="2"
                    class="w-full"
                    :placeholder="i18n.t('beamInput.lengthPlaceholder')"
                />
                <small class="hint">{{ i18n.t('beamInput.lengthHint') }}</small>
            </div>

            <!-- 2. Выбор ТИПА ОПОР -->
            <div class="field">
                <label for="support_type">{{ i18n.t('beamInput.supportType') }}</label>
                <Dropdown
                    v-model="formData.support_type"
                    id="support_type"
                    :options="supportTypes"
                    optionLabel="label"
                    optionValue="value"
                    :placeholder="i18n.t('beamInput.supportTypePlaceholder')"
                    class="w-full"
                />
                <small class="hint">{{ i18n.t('beamInput.supportTypeHint') }}</small>
            </div>

            <!-- 3. Поле СИЛЫ -->
            <div class="field">
                <label for="force">{{ i18n.t('beamInput.force') }}</label>
                <InputNumber 
                    v-model="formData.force" 
                    id="force"
                    :min="1" 
                    :max="10000"
                    :step="100"
                    :useGrouping="false"
                    mode="decimal"
                    class="w-full"
                    :placeholder="i18n.t('beamInput.forcePlaceholder')"
                />
                <small class="hint">{{ i18n.t('beamInput.forceHint') }}</small>
            </div>

            <!-- 4. Поле ПОЛОЖЕНИЯ СИЛЫ -->
            <div class="field">
                <label for="force_position">
                    {{ i18n.t('beamInput.forcePosition') }}
                </label>
                <InputNumber 
                    v-model="formData.force_position" 
                    id="force_position"
                    :min="0" 
                    :max="1" 
                    :step="0.01"
                    :useGrouping="false"
                    mode="decimal"
                    :minFractionDigits="2"
                    :maxFractionDigits="3"
                    class="w-full"
                    :placeholder="i18n.t('beamInput.forcePositionPlaceholder')"
                />
                <small class="hint">{{ i18n.t('beamInput.forcePositionHint') }}</small>
            </div>

            <!-- 5. Выбор ПРОФИЛЯ -->
            <div class="field">
                <label for="profile">{{ i18n.t('beamInput.profile') }}</label>
                <Dropdown
                    v-model="formData.profile_name"
                    id="profile"
                    :options="profileOptions"
                    optionLabel="name"
                    optionValue="key"
                    :placeholder="i18n.t('beamInput.profilePlaceholder')"
                    :loading="loadingProfiles"
                    class="w-full"
                />
                <small v-if="loadingProfiles" class="loading">
                    {{ i18n.t('beamInput.loadingProfiles') }}
                </small>
                <small v-else class="hint">
                    {{ i18n.t('beamInput.profileHint') }}
                </small>
            </div>

            <!-- 6. КНОПКА РАСЧЕТА -->
            <Button 
                type="submit" 
                :label="i18n.t('beamInput.calculate')"
                :loading="loading"
                :disabled="!isFormValid"
                class="w-full"
                icon="pi pi-calculator"
            />
        </form>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import InputNumber from 'primevue/inputnumber'
import Dropdown from 'primevue/dropdown'
import Button from 'primevue/button'

import { calculatorService } from '@/services/calculatorService'
import { i18n } from '@/services/i18n.service'
import type { BeamCalculationRequest, MaterialProfile } from '@/types/calculator'

const emit = defineEmits<{
    calculate: [data: BeamCalculationRequest]
}>()

// ============ ДАННЫЕ ФОРМЫ ============
// ИСПРАВЛЕНИЕ: Убедись, что все значения - ЧИСЛА, а не строки
const formData = ref<BeamCalculationRequest>({
    length: 5,           // число (метры)
    support_type: 'hinged', // строка
    force: 1000,         // ИЗМЕНИЛ: было 100, сделал 1000 (Н)
    force_position: 0.5, // число (доля от длины)
    profile_name: ''     // строка
})

// ============ UI СОСТОЯНИЕ ============
const profileOptions = ref<MaterialProfile[]>([])
const loadingProfiles = ref(false)
const loading = ref(false)
const errorMessage = ref<string>('')

// ============ ТИПЫ ОПОР ============
const supportTypes = i18n.getSupportTypes()

// ============ ВАЛИДАЦИЯ ============
const isFormValid = computed(() => {
    return formData.value.length > 0 &&
           formData.value.support_type &&
           formData.value.force > 0 &&
           formData.value.force_position >= 0 &&
           formData.value.force_position <= 1 &&
           formData.value.profile_name !== ''
})

// ============ ОТЛАДОЧНЫЙ ВЫВОД ============
// Добавляем watch для отладки значений
watch(formData, (newValue) => {
    console.log('Форма изменена:', {
        length: newValue.length,
        lengthType: typeof newValue.length,
        force: newValue.force,
        forceType: typeof newValue.force,
        force_position: newValue.force_position,
        forcePositionType: typeof newValue.force_position
    })
}, { deep: true })

// ============ ЗАГРУЗКА ПРОФИЛЕЙ ============
onMounted(async () => {
    loadingProfiles.value = true
    try {
        const response = await calculatorService.getProfiles()
        profileOptions.value = response.profiles
        
        // Выбираем первый профиль по умолчанию
        if (profileOptions.value.length > 0) {
            formData.value.profile_name = profileOptions.value[0].key
            console.log('Выбран профиль по умолчанию:', profileOptions.value[0].name)
        }
    } catch (error: any) {
        errorMessage.value = i18n.t('errors.backendError', { 
            message: error.message 
        })
        console.error('Ошибка загрузки профилей:', error)
    } finally {
        loadingProfiles.value = false
    }
})

// ============ ОТПРАВКА ФОРМЫ ============
const handleSubmit = async () => {
    if (!formData.value.profile_name) {
        errorMessage.value = i18n.t('errors.noProfile')
        return
    }
    
    loading.value = true
    errorMessage.value = ''
    
    try {
        // ВАЖНО: Проверяем, что отправляем числа, а не строки
        const dataToSend = {
            ...formData.value,
            // Принудительно приводим к числам (на всякий случай)
            length: Number(formData.value.length),
            force: Number(formData.value.force),
            force_position: Number(formData.value.force_position)
        }
        
        console.log('Отправляемые данные:', dataToSend)
        console.log('JSON для отправки:', JSON.stringify(dataToSend))
        
        // Эмитим событие с данными
        emit('calculate', dataToSend)
        
    } catch (error: any) {
        errorMessage.value = i18n.t('errors.calculationFailed', { 
            message: error.message 
        })
        console.error('Ошибка отправки формы:', error)
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
.beam-input-form {
    padding: 1.5rem;
    background: #f9fafb;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}

.field {
    margin-bottom: 1.5rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: #374151;
}

/* Подсказки под полями */
.hint {
    display: block;
    margin-top: 0.25rem;
    color: #6b7280;
    font-size: 0.875rem;
}

/* Сообщение загрузки */
.loading {
    display: block;
    margin-top: 0.25rem;
    color: #3b82f6;
    font-size: 0.875rem;
}

/* Сообщение об ошибке */
.error-message {
    background: #fef2f2;
    color: #dc2626;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    border: 1px solid #fecaca;
    font-size: 0.875rem;
}

/* Стили для PrimeVUE компонентов */
:deep(.p-inputnumber) {
    width: 100%;
}

:deep(.p-dropdown) {
    width: 100%;
}

:deep(.p-button) {
    width: 100%;
    padding: 0.75rem;
    font-weight: 600;
}

/* Улучшаем внешний вид InputNumber */
:deep(.p-inputnumber-input) {
    padding: 0.75rem;
    border-radius: 8px;
    border: 1px solid #d1d5db;
    transition: border-color 0.2s;
}

:deep(.p-inputnumber-input:focus) {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Кнопки вверх/вниз в InputNumber */
:deep(.p-inputnumber-button) {
    background: #f3f4f6;
    border: 1px solid #d1d5db;
    color: #374151;
}

:deep(.p-inputnumber-button:hover) {
    background: #e5e7eb;
}
</style>