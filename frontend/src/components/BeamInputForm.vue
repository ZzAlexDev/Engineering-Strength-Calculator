<template>
    <div class="beam-input-form">
        <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
        </div>
        
        <form @submit.prevent="handleSubmit">
            <div class="field">
                <label for="length">{{ i18n.t('beamInput.length') }}</label>
                <InputNumber 
                    v-model="formData.length" 
                    id="length"
                    :min="0.1" 
                    :max="50" 
                    :step="0.1"
                    :useGrouping="false"
                />
            </div>

            <div class="field">
                <label for="support_type">{{ i18n.t('beamInput.supportType') }}</label>
                <Dropdown
                    v-model="formData.support_type"
                    id="support_type"
                    :options="supportTypes"
                    optionLabel="label"
                    optionValue="value"
                    :placeholder="i18n.t('beamInput.supportType')"
                />
            </div>

            <div class="field">
                <label for="force">{{ i18n.t('beamInput.force') }}</label>
                <InputNumber 
                    v-model="formData.force" 
                    id="force"
                    :min="1" 
                    :max="1000" 
                    :step="1"
                    :useGrouping="false"
                />
            </div>

            <div class="field">
                <label for="force_position">
                    {{ i18n.t('beamInput.forcePosition') }}
                    <small>{{ i18n.t('beamInput.forcePositionHint') }}</small>
                </label>
                <InputNumber 
                    v-model="formData.force_position" 
                    id="force_position"
                    :min="0" 
                    :max="1" 
                    :step="0.01"
                    :useGrouping="false"
                />
            </div>

            <div class="field">
                <label for="profile">{{ i18n.t('beamInput.profile') }}</label>
                <Dropdown
                    v-model="formData.profile_name"
                    id="profile"
                    :options="profileOptions"
                    optionLabel="name"
                    optionValue="key"
                    :placeholder="i18n.t('beamInput.profile')"
                    :loading="loadingProfiles"
                />
                <small v-if="loadingProfiles">
                    {{ i18n.t('beamInput.loadingProfiles') }}
                </small>
            </div>

            <Button 
                type="submit" 
                :label="i18n.t('beamInput.calculate')"
                :loading="loading"
                :disabled="!isFormValid"
            />
        </form>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import InputNumber from 'primevue/inputnumber'
import Dropdown from 'primevue/dropdown'
import Button from 'primevue/button'

import { calculatorService } from '@/services/calculatorService'
import { i18n } from '@/services/i18n.service'
import type { BeamCalculationRequest, MaterialProfile } from '@/types/calculator'

const emit = defineEmits<{
    calculate: [data: BeamCalculationRequest]
}>()

// Данные формы
const formData = ref<BeamCalculationRequest>({
    length: 5,
    support_type: 'hinged',
    force: 100,
    force_position: 0.5,
    profile_name: ''
})

// UI состояние
const profileOptions = ref<MaterialProfile[]>([])
const loadingProfiles = ref(false)
const loading = ref(false)
const errorMessage = ref<string>('')

// Типы опор
const supportTypes = i18n.getSupportTypes()

// Валидация
const isFormValid = computed(() => {
    return formData.value.length > 0 &&
           formData.value.support_type &&
           formData.value.force > 0 &&
           formData.value.profile_name
})

// Загрузка профилей
onMounted(async () => {
    loadingProfiles.value = true
    try {
        const response = await calculatorService.getProfiles()
        profileOptions.value = response.profiles
        
        if (profileOptions.value.length > 0) {
            formData.value.profile_name = profileOptions.value[0].key
        }
    } catch (error: any) {
        errorMessage.value = i18n.t('errors.backendError', { 
            message: error.message 
        })
    } finally {
        loadingProfiles.value = false
    }
})

// Отправка формы
const handleSubmit = async () => {
    if (!formData.value.profile_name) {
        errorMessage.value = i18n.t('errors.noProfile')
        return
    }
    
    loading.value = true
    errorMessage.value = ''
    
    try {
        emit('calculate', formData.value)
    } catch (error: any) {
        errorMessage.value = i18n.t('errors.calculationFailed', { 
            message: error.message 
        })
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
.beam-input-form {
    padding: 1rem;
}

.field {
    margin-bottom: 1.5rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
}

small {
    display: block;
    margin-top: 0.25rem;
    color: #666;
}

.error-message {
    background: #fee;
    color: #c00;
    padding: 0.75rem;
    border-radius: 4px;
    margin-bottom: 1rem;
}
</style>