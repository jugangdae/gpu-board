<template>
  <v-card height="100%" elevation="2" class="pa-4 d-flex flex-column align-center justify-center">
    <div class="text-caption mb-2 font-weight-bold">TOTAL USERS</div>
    <div class="mt-1 text-h4">
      <template v-if="SIMPLE_DATA !== null">{{ SIMPLE_DATA }}</template>
      <template v-else>...</template>
    </div>
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

const API_URL = 'http://localhost:8000/api/sample/users'
const SIMPLE_DATA = ref(null)

async function fetch() {
  try {
    const res = await axios.get(API_URL)
    console.log(Object.keys(res.data).length)

    SIMPLE_DATA.value = Object.keys(res.data).length
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