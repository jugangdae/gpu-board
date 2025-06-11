<template>
  <v-dialog v-model="model" max-width="1200" persistent>
    <v-card>
      <v-card-title>
        보고서 (시스템/차트/랭크)
        <v-spacer/>
        <v-btn icon @click="model=false"><v-icon>mdi-close</v-icon></v-btn>
      </v-card-title>
      <v-card-text>
        <!-- 시스템 info -->
        <v-card class="mb-4 pa-3">
          <div class="text-h6 mb-2">System Info</div>
          <div>총 유저수: <b>{{ sysinfo.user_count }}</b></div>
          <div>GPU: <b>{{ sysinfo.gpu_count }}</b> ({{ sysinfo.gpu_models?.join(', ') }})</div>
          <div>CPU: <b>{{ sysinfo.cpu_count }}</b> ({{ sysinfo.cpu_models?.join(', ') }})</div>
          <div>Memory: <b>{{ sysinfo.memory_count }}</b> ({{ sysinfo.memory_total_tb }}TB)</div>
          <div>
            GPU 사용중: {{ sysinfo.gpu_used }} /
            CPU 사용중: {{ sysinfo.cpu_used }} /
            Memory 사용중: {{ sysinfo.memory_used }}
          </div>
        </v-card>

        <!-- system info 아래 도넛 차트 3개 -->
        <v-row class="mb-4 mt-2" style="justify-content:center;">
          <v-col cols="12" md="4" style="display: flex; justify-content: center;">
            <DonutChart
              :used="sysinfo.gpu_used || 0"
              :total="sysinfo.gpu_count || 0"
              label="GPU"
              color="#8e24aa"
            />
          </v-col>
          <v-col cols="12" md="4" style="display: flex; justify-content: center;">
            <DonutChart
              :used="sysinfo.cpu_used || 0"
              :total="sysinfo.cpu_count || 0"
              label="CPU"
              color="#1976d2"
            />
          </v-col>
          <v-col cols="12" md="4" style="display: flex; justify-content: center;">
            <DonutChart
              :used="sysinfo.memory_used || 0"
              :total="sysinfo.memory_count || 0"
              label="Memory"
              color="#43a047"
            />
          </v-col>
        </v-row>

        <!-- 전체 사용량 라인차트 -->
        <LineChart v-if="usageLoaded"
          :chart-data="totalUsageChartData"
          :options="lineOptions"
          title="전체 자원 사용량 (GPU/CPU/Memory)" />
        <div v-else>Loading...</div>

        <!-- 개별 사용량 라인차트 -->
        <v-row>
          <v-col cols="12" md="4">
            <v-card class="pa-3 mb-2">
              <div class="d-flex align-center mb-2">
                <div class="text-h6">GPU 개별 사용량</div>
                <v-select :items="gpuNames" v-model="selectedGpu" label="GPU 선택" dense class="ml-4" style="max-width:150px" />
              </div>
              <LineChart v-if="gpuDetailChartData" :chart-data="gpuDetailChartData" :options="lineOptions" title="GPU 개별 사용량" />
            </v-card>
          </v-col>
          <v-col cols="12" md="4">
            <v-card class="pa-3 mb-2">
              <div class="d-flex align-center mb-2">
                <div class="text-h6">CPU 개별 사용량</div>
                <v-select :items="cpuNames" v-model="selectedCpu" label="CPU 선택" dense class="ml-4" style="max-width:150px" />
              </div>
              <LineChart v-if="cpuDetailChartData" :chart-data="cpuDetailChartData" :options="lineOptions" title="CPU 개별 사용량" />
            </v-card>
          </v-col>
          <v-col cols="12" md="4">
            <v-card class="pa-3 mb-2">
              <div class="d-flex align-center mb-2">
                <div class="text-h6">Memory 개별 사용량</div>
                <v-select :items="memoryNames" v-model="selectedMemory" label="Memory 선택" dense class="ml-4" style="max-width:150px" />
              </div>
              <LineChart v-if="memoryDetailChartData" :chart-data="memoryDetailChartData" :options="lineOptions" title="Memory 개별 사용률(%)" />
            </v-card>
          </v-col>
        </v-row>

        <!-- 온도/사용률 -->
        <v-row>
          <v-col cols="12" md="4">
            <v-card class="pa-3">
              <div class="text-h6 mb-2">GPU 온도(°C)</div>
              <ul>
                <li v-for="(t, i) in gpuTemps" :key="i">
                  <span :style="{ color: getTempColor(t) }">
                    {{ gpuNames[i] }}: <b>{{ t }}°C</b>
                  </span>
                </li>
              </ul>
            </v-card>
          </v-col>
          <v-col cols="12" md="4">
            <v-card class="pa-3">
              <div class="text-h6 mb-2">CPU 온도(°C)</div>
              <ul>
                <li v-for="(t, i) in cpuTemps" :key="i">
                  <span :style="{ color: getTempColor(t) }">
                    {{ cpuNames[i] }}: <b>{{ t }}°C</b>
                  </span>
                </li>
              </ul>
            </v-card>
          </v-col>
          <v-col cols="12" md="4">
            <v-card class="pa-3">
              <div class="text-h6 mb-2">Memory 사용률(%)</div>
              <ul>
                <li v-for="(t, i) in memoryUsages" :key="i">
                  <span style="color: #1976d2">
                    {{ memoryNames[i] }}: <b>{{ t }}%</b>
                  </span>
                </li>
              </ul>
            </v-card>
          </v-col>
        </v-row>

        <!-- 사용자 랭크 -->
        <v-card class="mt-6">
          <div class="text-h6 pa-3">사용자 랭크 (누적 사용량)</div>
          <v-table>
            <thead>
              <tr>
                <th>순위</th>
                <th>이름</th>
                <th>GPU 사용일</th>
                <th>CPU 사용일</th>
                <th>Memory 사용일</th>
                <th>리포트</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(u, i) in userRank" :key="u.name">
                <td>{{ i+1 }}</td>
                <td>{{ u.name }}</td>
                <td>{{ u.gpu }}</td>
                <td>{{ u.cpu }}</td>
                <td>{{ u.memory }}</td>
                <td>
                  <a :href="'/report/user/' + u.name" target="_blank">보고서</a>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-card>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import axios from 'axios'
import LineChart from './LineChart.vue'
import DonutChart from './DonutChart.vue'

const model = defineModel()
const sysinfo = ref({})
const totalUsage = ref({ dates: [], gpu: [], cpu: [], memory: [] })
const usageLoaded = ref(false)
const gpuNames = ref([])
const cpuNames = ref([])
const memoryNames = ref([])
const selectedGpu = ref('')
const selectedCpu = ref('')
const selectedMemory = ref('')
const gpuDetail = ref({ dates: [], values: [] })
const cpuDetail = ref({ dates: [], values: [] })
const memoryDetail = ref({ dates: [], values: [] })
const gpuTemps = ref([])
const cpuTemps = ref([])
const memoryUsages = ref([])
const userRank = ref([])

const lineOptions = {
  responsive: true,
  plugins: { legend: { display: true } },
  scales: { y: { beginAtZero: true } }
}

async function fetchAll() {
  sysinfo.value = (await axios.get('http://127.0.0.1:5000/api/report/sysinfo')).data
  const usage = (await axios.get('http://127.0.0.1:5000/api/report/total_usage')).data
  totalUsage.value = usage
  usageLoaded.value = true
  await fetchStatus()
  userRank.value = (await axios.get('http://127.0.0.1:5000/api/report/rank')).data
  fetchIndividualDetails()
}
onMounted(fetchAll)

// 3초마다 온도/사용률 최신화
async function fetchStatus() {
  const status = (await axios.get('http://127.0.0.1:5000/api/report/status')).data
  gpuNames.value = status.gpu_names
  cpuNames.value = status.cpu_names
  memoryNames.value = status.memory_names
  gpuTemps.value = status.gpu_temps
  cpuTemps.value = status.cpu_temps
  memoryUsages.value = status.memory_usages
  if (!selectedGpu.value) selectedGpu.value = gpuNames.value[0]
  if (!selectedCpu.value) selectedCpu.value = cpuNames.value[0]
  if (!selectedMemory.value) selectedMemory.value = memoryNames.value[0]
  setTimeout(fetchStatus, 3000)
}

async function fetchIndividualDetails() {
  if (selectedGpu.value) {
    gpuDetail.value = (await axios.get('http://127.0.0.1:5000/api/report/individual_usage', { params: { type: "GPU", name: selectedGpu.value } })).data
  }
  if (selectedCpu.value) {
    cpuDetail.value = (await axios.get('http://127.0.0.1:5000/api/report/individual_usage', { params: { type: "CPU", name: selectedCpu.value } })).data
  }
  if (selectedMemory.value) {
    memoryDetail.value = (await axios.get('http://127.0.0.1:5000/api/report/individual_usage', { params: { type: "Memory", name: selectedMemory.value } })).data
  }
}
watch(selectedGpu, fetchIndividualDetails)
watch(selectedCpu, fetchIndividualDetails)
watch(selectedMemory, fetchIndividualDetails)

const totalUsageChartData = computed(() => ({
  labels: totalUsage.value.dates,
  datasets: [
    {
      label: "GPU 전체 사용량",
      data: totalUsage.value.gpu,
      fill: false,
      tension: 0.4,
      borderColor: "#8e24aa",
      backgroundColor: "#8e24aa"
    },
    {
      label: "CPU 전체 사용량",
      data: totalUsage.value.cpu,
      fill: false,
      tension: 0.4,
      borderColor: "#1976d2",
      backgroundColor: "#1976d2"
    },
    {
      label: "Memory 전체 사용량",
      data: totalUsage.value.memory,
      fill: false,
      tension: 0.4,
      borderColor: "#43a047",
      backgroundColor: "#43a047"
    }
  ]
}))
const gpuDetailChartData = computed(() => ({
  labels: gpuDetail.value.dates,
  datasets: [
    {
      label: selectedGpu.value + " 사용량",
      data: gpuDetail.value.values,
      fill: false,
      tension: 0.4,
      borderColor: "#8e24aa",
      backgroundColor: "#8e24aa"
    }
  ]
}))
const cpuDetailChartData = computed(() => ({
  labels: cpuDetail.value.dates,
  datasets: [
    {
      label: selectedCpu.value + " 사용량",
      data: cpuDetail.value.values,
      fill: false,
      tension: 0.4,
      borderColor: "#1976d2",
      backgroundColor: "#1976d2"
    }
  ]
}))
const memoryDetailChartData = computed(() => ({
  labels: memoryDetail.value.dates,
  datasets: [
    {
      label: selectedMemory.value + " 사용률(%)",
      data: memoryDetail.value.values,
      fill: false,
      tension: 0.4,
      borderColor: "#43a047",
      backgroundColor: "#43a047"
    }
  ]
}))

// 온도 색상
function getTempColor(t) {
  if (t <= 40) return "#43a047"
  if (t <= 60) return "#ffc107"
  return "#d32f2f"
}
</script>
