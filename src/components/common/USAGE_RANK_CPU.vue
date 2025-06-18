<template>
  <v-card class="pa-4" elevation="2">
    <div class="font-weight-bold mb-2">CPU 사용률 TOP5</div>
    <v-table density="compact">
      <thead>
        <tr>
          <th>순위</th>
          <th>사용자</th>
          <th>사용량(%)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(user, idx) in SIMPLE_DATA" :key="user.user">
          <td>{{ idx + 1 }}</td>
          <td>
            <router-link :to="`/user/${user.user}/report`">{{ user.user }}</router-link>
          </td>
          <td>
            <v-progress-linear :model-value="user.value" :color="getColor(user.value, 'primary')" height="16" striped>
              {{ user.value }}%
            </v-progress-linear>
          </td>
        </tr>
        <tr v-if="!SIMPLE_DATA.length">
          <td colspan="3"><v-skeleton-loader type="table-row" /></td>
        </tr>
      </tbody>
    </v-table>
  </v-card>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'

const props = defineProps({
  startDate: {
    type: String,
    required: true,
    validator: (value) => /^\d{8}$/.test(value), // YYYYMMDD 형식 검증
  },
  endDate: {
    type: String,
    required: true,
    validator: (value) => /^\d{8}$/.test(value), // YYYYMMDD 형식 검증
  },
});

const API_URL = 'http://localhost:8000/api/cpu_user_rank'
const SIMPLE_DATA = ref([])
const WARNING_LEVEL = 70
const DANGER_LEVEL = 90

function getColor(val, color) {
  if (val >= DANGER_LEVEL) return 'red'
  if (val >= WARNING_LEVEL) return 'orange'
  return color //'primary'
}

async function fetch() {
  try {
    const res = await axios.get(API_URL)
    SIMPLE_DATA.value = res.data.users.sort((a, b) => b.value - a.value).slice(0, 5)
  } catch { SIMPLE_DATA.value = [] }
}


watch([() => props.startDate, () => props.endDate], async () => {
  fetch();
});

onMounted(() => {
  fetch()
})
</script>