<template>
  <div>
    <div class="text-h6 mb-2">{{ title }}</div>
    <canvas ref="canvas" />
  </div>
</template>
<script setup>
import { ref, watch, onMounted } from 'vue'
import { Chart, LineController, LineElement, PointElement, LinearScale, Title, CategoryScale, Legend } from 'chart.js'
Chart.register(LineController, LineElement, PointElement, LinearScale, Title, CategoryScale, Legend)

const props = defineProps({
  chartData: Object,
  options: Object,
  title: String
})
const canvas = ref(null)
let chartInstance = null

function renderChart() {
  if (chartInstance) chartInstance.destroy()
  chartInstance = new Chart(canvas.value, {
    type: 'line',
    data: props.chartData,
    options: props.options
  })
}
onMounted(renderChart)
watch(() => props.chartData, renderChart, { deep: true })
</script>
