<template>
  <div style="width: 180px; margin: 0 auto; text-align: center;">
    <canvas ref="canvas" />
    <div class="mt-2" style="font-size:1.1em;">
      <span>{{ label }}</span><br />
      <b>{{ used }}</b> / {{ total }}
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { Chart, DoughnutController, ArcElement, Tooltip, Legend } from 'chart.js'
Chart.register(DoughnutController, ArcElement, Tooltip, Legend)

const props = defineProps({
  used: Number,
  total: Number,
  label: String,
  color: String // 사용중 색
})
const canvas = ref(null)
let chartInstance = null

function renderChart() {
  if (chartInstance) chartInstance.destroy()
  chartInstance = new Chart(canvas.value, {
    type: 'doughnut',
    data: {
      labels: ['사용 중', '유휴'],
      datasets: [
        {
          data: [props.used, props.total - props.used],
          backgroundColor: [props.color, '#eee'],
          borderWidth: 0
        }
      ]
    },
    options: {
      cutout: '75%',
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: function(context) {
              if (context.dataIndex === 0)
                return `사용 중: ${props.used}개`
              else
                return `유휴: ${props.total - props.used}개`
            }
          }
        }
      }
    }
  })
}
onMounted(renderChart)
watch(() => [props.used, props.total], renderChart)
</script>
