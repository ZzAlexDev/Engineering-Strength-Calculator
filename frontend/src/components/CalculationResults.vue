<template>
  <div v-if="result" class="calculation-results">
    <Card>
      <template #title>{{ i18n.t('results.title') }}</template>
      <template #content>
        <!-- Секция 1: Исходные данные -->
        <div class="section">
          <h3>{{ i18n.t('results.inputData') }}</h3>
          <DataTable :value="inputData" showGridlines>
            <Column field="parameter" :header="i18n.t('results.parameter')" />
            <Column field="value" :header="i18n.t('results.value')" />
          </DataTable>
        </div>
        
        <!-- Секция 2: Результаты расчета -->
        <div class="section">
          <h3>{{ i18n.t('results.calculationResults') }}</h3>
          <DataTable :value="calculationResults">
            <!-- Колонки результатов -->
          </DataTable>
        </div>
        
        <!-- Секция 3: Проверка по нормам -->
        <div class="section">
          <h3>{{ i18n.t('results.verification') }}</h3>
          <div class="verification-status">
            <Badge :value="strengthStatus" :severity="strengthSeverity" />
            <Badge :value="stiffnessStatus" :severity="stiffnessSeverity" />
          </div>
        </div>
        
        <!-- Секция 4: Диаграмма -->
        <div class="section">
          <BeamDiagram :diagramData="result.diagram_data" />
        </div>
      </template>
    </Card>
  </div>
</template>