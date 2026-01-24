<template>
    <div class="language-switcher">
        <Button 
            :label="currentLabel" 
            @click="toggleLanguage"
            outlined
            size="small"
        />
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Button from 'primevue/button'
import { i18n } from '@/services/i18n.service'

// Используем computed, чтобы Vue отслеживал изменения
const currentLanguage = computed(() => i18n.getLocale())

// Метка с флагом/иконкой
const currentLabel = computed(() => {
    return currentLanguage.value === 'ru' ? 'RU' : 'EN'
})

const toggleLanguage = () => {
    const newLang = currentLanguage.value === 'ru' ? 'en' : 'ru'
    i18n.setLocale(newLang)
    
    // Принудительно обновляем страницу (на первое время)
    // location.reload() // Раскомментировать, если не помогает
}
</script>

<style scoped>
.language-switcher {
    display: inline-block;
}
</style>