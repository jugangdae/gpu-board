<template>
  <v-card class="pa-4" elevation="2">
    <div class="font-weight-bold mb-2">IDLE TIME TOP5 사용자</div>
    <v-table density="compact">
      <thead>
        <tr>
          <th>순위</th>
          <th>사용자</th>
          <th>IdleTime(분)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(user, idx) in SIMPLE_DATA" :key="user.user">
          <td>{{ idx + 1 }}</td>
          <td>
            <router-link :to="`/user/${user.user}/report`">{{ user.user }}</router-link>

          </td>
          <td>
            {{ user.value }}
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

const API_URL = 'http://localhost:8000/api/idle_user_rank'
const SIMPLE_DATA = ref([])

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