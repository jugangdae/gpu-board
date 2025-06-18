<template>
  <v-container>
    <!-- 날짜 범위 선택 -->
    <v-row class="mb-6">
      <v-col cols="12" md="5">
        <v-menu v-model="startDateMenu" :close-on-content-click="false" transition="scale-transition">
          <template #activator="{ props }">
            <v-text-field v-model="selectedStartDate" label="시작 날짜" prepend-icon="mdi-calendar" readonly v-bind="props" hide-details />
          </template>
          <v-date-picker v-model="selectedStartDate" type="string" @update:modelValue="date => { startDateMenu = false; selectedStartDate = formatDateToString(date); }" locale="ko-KR" />
        </v-menu>
      </v-col>
      <v-col cols="12" md="5">
        <v-menu v-model="endDateMenu" :close-on-content-click="false" transition="scale-transition">
          <template #activator="{ props }">
            <v-text-field v-model="selectedEndDate" label="종료 날짜" prepend-icon="mdi-calendar" readonly v-bind="props" hide-details />
          </template>
          <v-date-picker v-model="selectedEndDate" type="string" @update:modelValue="date => { endDateMenu = false; selectedEndDate = formatDateToString(date); }" locale="ko-KR" />
        </v-menu>
      </v-col>
      <v-col cols="12" md="2" class="d-flex align-center">
        <v-btn color="primary" class="mr-2" @click="setThisYear">올해 전체</v-btn>
        <v-btn color="info" @click="reloadAll">새로고침</v-btn>
      </v-col>
    </v-row>

    <!-- 전체 GPU/CPU/MEM 사용량 멀티 차트 (시계열) -->
    <v-row>
      <v-col cols="12">
        <MULTI_CHART_JS :startDate="startDateStr" :endDate="endDateStr"/>
      </v-col>
    </v-row>

    <!-- 각 개별 리소스(예: GPU 0~n, CPU 0~n, MEM 0~n 등) 싱글차트 예시 -->
    <v-row>
      <v-col cols="12" md="4">
        <SINGLE_CHART_JS :startDate="startDateStr" :endDate="endDateStr" :chartTitle="'GPU 0 개별 사용량'" />
      </v-col>
      <v-col cols="12" md="4">
        <SINGLE_CHART_JS :startDate="startDateStr" :endDate="endDateStr" :chartTitle="'CPU 0 개별 사용량'" />
      </v-col>
      <v-col cols="12" md="4">
        <SINGLE_CHART_JS :startDate="startDateStr" :endDate="endDateStr" :chartTitle="'MEM 0 개별 사용량'" />
      </v-col>
    </v-row>

    <!-- GPU 온도(개별) 예시 -->
    <v-row>
      <v-col cols="12" md="6">
        <SINGLE_CHART_JS :startDate="startDateStr" :endDate="endDateStr" :chartTitle="'GPU 0 온도'" />
      </v-col>
    </v-row>

    <!-- 리소스/유저 간단 현황 카드 예시 -->
    <v-row>
      <v-col cols="12" md="3"><SIMPLE_GPU_COUNT :startDate="startDateStr" :endDate="endDateStr"/></v-col>
      <v-col cols="12" md="3"><SIMPLE_CPU_COUNT :startDate="startDateStr" :endDate="endDateStr"/></v-col>
      <v-col cols="12" md="3"><SIMPLE_TOTAL_MEM :startDate="startDateStr" :endDate="endDateStr"/></v-col>
      <v-col cols="12" md="3"><SIMPLE_TOTAL_CPU :startDate="startDateStr" :endDate="endDateStr"/></v-col>
    </v-row>

    <!-- 랭킹(유저 TOP5 등) -->
    <v-row>
      <v-col cols="12" md="3"><USAGE_RANK_GPU :startDate="startDateStr" :endDate="endDateStr"/></v-col>
      <v-col cols="12" md="3"><USAGE_RANK_CPU :startDate="startDateStr" :endDate="endDateStr"/></v-col>
      <v-col cols="12" md="3"><USAGE_RANK_MEM :startDate="startDateStr" :endDate="endDateStr"/></v-col>
      <v-col cols="12" md="3"><USAGE_RANK_IDLE :startDate="startDateStr" :endDate="endDateStr"/></v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import MULTI_CHART_JS from '@/components/common/MULTI_CHART_JS.vue'
import SINGLE_CHART_JS from '@/components/common/SINGLE_CHART_JS.vue'
import SIMPLE_GPU_COUNT from '@/components/common/SIMPLE_GPU_COUNT.vue'
import SIMPLE_CPU_COUNT from '@/components/common/SIMPLE_CPU_COUNT.vue'
import SIMPLE_TOTAL_MEM from '@/components/common/SIMPLE_TOTAL_MEM.vue'
import SIMPLE_TOTAL_CPU from '@/components/common/SIMPLE_TOTAL_CPU.vue'
import USAGE_RANK_GPU from '@/components/common/USAGE_RANK_GPU.vue'
import USAGE_RANK_CPU from '@/components/common/USAGE_RANK_CPU.vue'
import USAGE_RANK_MEM from '@/components/common/USAGE_RANK_MEM.vue'
import USAGE_RANK_IDLE from '@/components/common/USAGE_RANK_IDLE.vue'

// 날짜 상태
const today = new Date()
const thisYear = today.getFullYear()
const selectedStartDate = ref(`${thisYear}-01-01`)
const selectedEndDate = ref(`${thisYear}-12-31`)
const startDateMenu = ref(false)
const endDateMenu = ref(false)

// YYYY-MM-DD → YYYYMMDD 변환
const toYYYYMMDD = date => (typeof date === 'string' ? date.replace(/-/g, '') : '')
const startDateStr = computed(() => toYYYYMMDD(selectedStartDate.value))
const endDateStr = computed(() => toYYYYMMDD(selectedEndDate.value))

function formatDateToString(date) {
  if (!date) return ''
  if (typeof date === 'string') return date
  if (date instanceof Date) {
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
  }
  return ''
}
function setThisYear() {
  selectedStartDate.value = `${thisYear}-01-01`
  selectedEndDate.value = `${thisYear}-12-31`
}
function reloadAll() {}
</script>
