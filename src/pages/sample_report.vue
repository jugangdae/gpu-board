<template>
  <v-container fluid class="pa-4" style="height:100vh;width:100vw;">

    <!-- 날짜 선택 UI -->
    <v-row class="mb-4">
      <v-col cols="12" md="6">
        <v-menu v-model="startDateMenu" :close-on-content-click="false" transition="scale-transition" offset-y
          min-width="auto">
          <template v-slot:activator="{ props }">
            <v-text-field v-model="selectedStartDate" label="시작 날짜" prepend-icon="mdi-calendar" readonly v-bind="props"
              hide-details />
          </template>
          <v-date-picker v-model="selectedStartDate" type="string" no-title scrollable
            @update:modelValue="date => { startDateMenu = false; selectedStartDate = formatDateToString(date); }"
            locale="ko-KR" />
        </v-menu>
      </v-col>
      <v-col cols="12" md="6">
        <v-menu v-model="endDateMenu" :close-on-content-click="false" transition="scale-transition" offset-y
          min-width="auto">
          <template v-slot:activator="{ props }">
            <v-text-field v-model="selectedEndDate" label="종료 날짜" prepend-icon="mdi-calendar" readonly v-bind="props"
              hide-details />
          </template>
          <v-date-picker v-model="selectedEndDate" type="string" no-title scrollable
            @update:modelValue="date => { endDateMenu = false; selectedEndDate = formatDateToString(date); }"
            locale="ko-KR" />
        </v-menu>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-card-text class="py-4">
          <span style="font-size: 200%;">
            README: 리포트 페이지 구현 참고용
          </span>
        </v-card-text>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <SIMPLE_UPDATE_1 :startDate="selectedStartDate ? selectedStartDate.replace(/-/g, '') : ''"
          :endDate="selectedEndDate ? selectedEndDate.replace(/-/g, '') : ''" />
      </v-col>
      <v-col>
        <SIMPLE_UPDATE_2 :startDate="selectedStartDate ? selectedStartDate.replace(/-/g, '') : ''"
          :endDate="selectedEndDate ? selectedEndDate.replace(/-/g, '') : ''" />
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <!-- selectedStartDate의 값을 직접 YYYYMMDD로 변환하여 전달 -->
        <MULTI_CHART_JS :startDate="selectedStartDate ? selectedStartDate.replace(/-/g, '') : ''"
          :endDate="selectedEndDate ? selectedEndDate.replace(/-/g, '') : ''" />
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <!-- selectedStartDate의 값을 직접 YYYYMMDD로 변환하여 전달 -->
        <SINGLE_CHART_JS :startDate="selectedStartDate ? selectedStartDate.replace(/-/g, '') : ''"
          :endDate="selectedEndDate ? selectedEndDate.replace(/-/g, '') : ''" />
      </v-col>
    </v-row>

  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue';
import MULTI_CHART_JS from '@/components/common/MULTI_CHART_JS.vue'; // 실제 경로에 맞게 수정
import SINGLE_CHART_JS from '@/components/common/SINGLE_CHART_JS.vue';
import SIMPLE_UPDATE_1 from '@/components/common/SIMPLE_UPDATE_1.vue';
import SIMPLE_UPDATE_2 from '@/components/common/SIMPLE_UPDATE_2.vue';

const selectedStartDate = ref('2025-01-01');
const selectedEndDate = ref('2025-01-31');
const startDateMenu = ref(false);
const endDateMenu = ref(false);

function formatDateToString(date) {
  if (!date) return ''; // null 또는 undefined 처리
  if (typeof date === 'string') return date; // 이미 문자열이면 그대로 반환

  if (date instanceof Date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }
  return ''; // 그 외의 경우 (예: 숫자가 들어온 경우)
}

</script>