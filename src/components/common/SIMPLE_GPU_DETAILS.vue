<template>
  <v-card class="pa-4" elevation="2">
    <div class="font-weight-bold mb-2">GPU 상세</div>
    <v-table density="compact">
      <thead>
        <tr>
          <th>ID</th>
          <th>NAME</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(gpus, idx) in SIMPLE_DATA" :key="gpus.id">
          <td>
            {{ gpus.id }}
          </td>
          <td>
            {{ gpus.name }}
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

const API_URL = 'http://localhost:8000/api/sample/gpus'
const SIMPLE_DATA = ref([])

async function fetch() {
  try {
    const res = await axios.get(API_URL)
    SIMPLE_DATA.value = res.data
  } catch (e) {
    SIMPLE_DATA.value = null
  }
}

watch([() => props.startDate, () => props.endDate], async () => {
  fetch();
});

onMounted(() => {
  fetch()
})
</script>

<style scoped>
.caption {
  font-size: 0.85rem;
}
</style>