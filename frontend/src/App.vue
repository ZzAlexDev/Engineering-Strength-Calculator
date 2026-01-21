<template>
  <div id="app">
    <header class="app-header">
      <div class="header-content">
        <h1>🧮 Engineering Strength Calculator</h1>
        <div class="header-actions">
          <Button label="Документация" icon="pi pi-book" text />
        </div>
      </div>
    </header>

    <main class="app-main">
      <div class="container">
        <div class="calculator-layout">
          <!-- Левая колонка: Форма ввода -->
          <div class="input-section">
            <div class="placeholder">
              <i class="pi pi-sliders-h" style="font-size: 3rem; color: var(--surface-400);"></i>
              <h3>Форма ввода параметров</h3>
              <p>Здесь будет форма для ввода параметров балки</p>
            </div>
          </div>

          <!-- Правая колонка: Предпросмотр и результаты -->
          <div class="results-section">
            <div class="placeholder">
              <i class="pi pi-chart-bar" style="font-size: 3rem; color: var(--surface-400);"></i>
              <h3>Результаты расчёта</h3>
              <p>Здесь будут отображаться результаты и диаграммы</p>
            </div>
          </div>
        </div>
      </div>
    </main>

    <footer class="app-footer">
      <div class="container">
        <p>Engineering Strength Calculator v1.0.0 | MVP</p>
        <p>© 2026 | Создано с использованием Vue 3, TypeScript и FastAPI</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import Button from 'primevue/button'
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --primary-color: #3b82f6;
  --success-color: #10b981;
  --danger-color: #ef4444;
  --warning-color: #f59e0b;
}

body {
  font-family: 'Inter', sans-serif;
  background-color: #f8fafc;
  color: #334155;
}

.app-header {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  padding: 1rem 0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h1 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
}

.app-main {
  min-height: calc(100vh - 140px);
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.calculator-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.input-section, .results-section {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  min-height: 400px;
}

.placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  color: #64748b;
}

.placeholder h3 {
  margin-top: 1rem;
  margin-bottom: 0.5rem;
  color: #475569;
}

.placeholder p {
  max-width: 300px;
}

.app-footer {
  background: white;
  border-top: 1px solid #e2e8f0;
  padding: 1.5rem 0;
  text-align: center;
  color: #64748b;
  font-size: 0.875rem;
}

.app-footer p {
  margin-bottom: 0.25rem;
}

@media (max-width: 1024px) {
  .calculator-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .app-main {
    padding: 1rem 0;
  }
  
  .input-section, .results-section {
    padding: 1rem;
    min-height: 300px;
  }
}
</style>