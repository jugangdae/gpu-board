<template>
  <v-container>
    <h2>보고서</h2>
    <v-row class="mb-4">
      <v-col cols="12" md="4">
        <v-text-field v-model="startDate" label="시작일" type="date" :max="endDate"/>
      </v-col>
      <v-col cols="12" md="4">
        <v-text-field v-model="endDate" label="종료일" type="date" :min="startDate"/>
      </v-col>
      <v-col cols="12" md="2">
        <v-btn color="primary" class="mt-2" @click="fetchAllData">조회</v-btn>
      </v-col>
    </v-row>
    <v-card class="pa-4 mb-4">
      <h3>SYSTEM INFO</h3>
      <div>총 유저: {{ sysinfo.user_count }}명</div>
      <div>GPU: {{ sysinfo.gpu_total }}개 ({{ sysinfo.gpu_model }})</div>
      <div>CPU: {{ sysinfo.cpu_total }}개 ({{ sysinfo.cpu_model }})</div>
      <div>MEM: {{ sysinfo.mem_desc }}</div>
    </v-card>
    <v-row>
      <v-col>
        <LineChart :labels="dateLabels" :data="cpuUsage" title="CPU 전체 사용량"/>
      </v-col>
      <v-col>
        <LineChart :labels="dateLabels" :data="memUsage" title="MEM 전체 사용량"/>
      </v-col>
    </v-row>
    <v-card class="pa-4 my-4">
      <LineChart :labels="dateLabels" :data="gpuUsage" title="GPU 전체 사용량"/>
    </v-card>
    <v-row>
      <v-col>
        <h4>사용자 GPU 누적 사용 랭크</h4>
        <v-table>
          <thead><tr><th>사용자</th><th>총 사용량</th><th>리포트</th></tr></thead>
          <tbody>
            <tr v-for="r in rankUsage" :key="r.user">
              <td>{{ r.user }}</td>
              <td>{{ r.usage }}</td>
              <td><a :href="r.link" target="_blank">리포트</a></td>
            </tr>
          </tbody>
        </v-table>
      </v-col>
      <v-col>
        <h4>사용자 GPU 누적 유휴시간 랭크</h4>
        <v-table>
          <thead><tr><th>사용자</th><th>총 유휴시간</th><th>리포트</th></tr></thead>
          <tbody>
            <tr v-for="r in rankIdle" :key="r.user">
              <td>{{ r.user }}</td>
              <td>{{ r.idle }}</td>
              <td><a :href="r.link" target="_blank">리포트</a></td>
            </tr>
          </tbody>
        </v-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import LineChart from '@/components/LineChart.vue'

const startDate = ref('2024-07-01')
const endDate = ref('2024-07-31')
const sysinfo = ref({})
const dateLabels = ref([])
const cpuUsage = ref([])
const memUsage = ref([])
const gpuUsage = ref([])
const rankUsage = ref([])
const rankIdle = ref([])

async function fetchAllData() {
  sysinfo.value = (await axios.get('/api/sysinfo')).data
  const usage = (await axios.get('/api/reports/period', {
    params: { start: startDate.value, end: endDate.value }
  })).data
  dateLabels.value = usage.dates
  cpuUsage.value = usage.cpu_total
  memUsage.value = usage.mem_total
  gpuUsage.value = usage.gpu_total
  rankUsage.value = usage.rank_usage
  rankIdle.value = usage.rank_idle
}
fetchAllData()
</script>
