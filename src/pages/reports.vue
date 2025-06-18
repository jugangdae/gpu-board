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
        <SIMPLE_CPU_COUNT :startDate="selectedStartDate ? selectedStartDate.replace(/-/g, '') : ''"
          :endDate="selectedEndDate ? selectedEndDate.replace(/-/g, '') : ''" />
      </v-col>
      <v-col>
        <SIMPLE_GPU_COUNT :startDate="selectedStartDate ? selectedStartDate.replace(/-/g, '') : ''"
          :endDate="selectedEndDate ? selectedEndDate.replace(/-/g, '') : ''" />
      </v-col>
      <v-col>
        <SIMPLE_TOTAL_MEM :startDate="selectedStartDate ? selectedStartDate.replace(/-/g, '') : ''"
          :endDate="selectedEndDate ? selectedEndDate.replace(/-/g, '') : ''" />
      </v-col>
      <v-col>
        <SIMPLE_TOTAL_USER :startDate="selectedStartDate ? selectedStartDate.replace(/-/g, '') : ''"
          :endDate="selectedEndDate ? selectedEndDate.replace(/-/g, '') : ''" />
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <SIMPLE_GPU_DETAILS :startDate="selectedStartDate ? selectedStartDate.replace(/-/g, '') : ''"
          :endDate="selectedEndDate ? selectedEndDate.replace(/-/g, '') : ''" />
      </v-col>
    </v-row>


        <v-row>
      <v-col>
        <!-- selectedStartDate의 값을 직접 YYYYMMDD로 변환하여 전달 -->
        <SINGLE_CHART_CPU :startDate="selectedStartDate ? selectedStartDate.replace(/-/g, '') : ''"
          :endDate="selectedEndDate ? selectedEndDate.replace(/-/g, '') : ''" />
      </v-col>
      <v-col>
        <!-- selectedStartDate의 값을 직접 YYYYMMDD로 변환하여 전달 -->
        <SINGLE_CHART_MEM :startDate="selectedStartDate ? selectedStartDate.replace(/-/g, '') : ''"
          :endDate="selectedEndDate ? selectedEndDate.replace(/-/g, '') : ''" />
      </v-col>
      <v-col>
        <!-- selectedStartDate의 값을 직접 YYYYMMDD로 변환하여 전달 -->
        <SINGLE_CHART_GPU :startDate="selectedStartDate ? selectedStartDate.replace(/-/g, '') : ''"
          :endDate="selectedEndDate ? selectedEndDate.replace(/-/g, '') : ''" />
      </v-col>
    </v-row>


    <v-row>
      <v-col>
        <!-- selectedStartDate의 값을 직접 YYYYMMDD로 변환하여 전달 -->
        <MULTI_CHART_GPU :startDate="selectedStartDate ? selectedStartDate.replace(/-/g, '') : ''"
          :endDate="selectedEndDate ? selectedEndDate.replace(/-/g, '') : ''" />
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <!-- selectedStartDate의 값을 직접 YYYYMMDD로 변환하여 전달 -->
        <MULTI_CHART_TEMP :startDate="selectedStartDate ? selectedStartDate.replace(/-/g, '') : ''"
          :endDate="selectedEndDate ? selectedEndDate.replace(/-/g, '') : ''" />
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <USAGE_RANK_CPU :startDate="selectedStartDate ? selectedStartDate.replace(/-/g, '') : ''"
          :endDate="selectedEndDate ? selectedEndDate.replace(/-/g, '') : ''" />
      </v-col>
      <v-col>
        <USAGE_RANK_GPU :startDate="selectedStartDate ? selectedStartDate.replace(/-/g, '') : ''"
          :endDate="selectedEndDate ? selectedEndDate.replace(/-/g, '') : ''" />
      </v-col>
      <v-col>
        <USAGE_RANK_MEM :startDate="selectedStartDate ? selectedStartDate.replace(/-/g, '') : ''"
          :endDate="selectedEndDate ? selectedEndDate.replace(/-/g, '') : ''" />
      </v-col>
      <v-col>
        <USAGE_RANK_IDLE :startDate="selectedStartDate ? selectedStartDate.replace(/-/g, '') : ''"
          :endDate="selectedEndDate ? selectedEndDate.replace(/-/g, '') : ''" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue';
import MULTI_CHART_JS from '@/components/common/MULTI_CHART_JS.vue';
import MULTI_CHART_GPU from '@/components/common/MULTI_CHART_GPU.vue'; // 실제 경로에 맞게 수정
import MULTI_CHART_TEMP from '@/components/common/MULTI_CHART_TEMP.vue';
import SINGLE_CHART_CPU from '@/components/common/SINGLE_CHART_CPU.vue';
import SINGLE_CHART_GPU from '@/components/common/SINGLE_CHART_GPU.vue';
import SINGLE_CHART_MEM from '@/components/common/SINGLE_CHART_MEM.vue';
// import SIMPLE_UPDATE_1 from '@/components/common/SIMPLE_UPDATE_1.vue';
import SIMPLE_CPU_COUNT from '@/components/common/SIMPLE_CPU_COUNT.vue';
import SIMPLE_GPU_COUNT from '@/components/common/SIMPLE_GPU_COUNT.vue';
import SIMPLE_TOTAL_MEM from '@/components/common/SIMPLE_TOTAL_MEM.vue';
import SIMPLE_TOTAL_USER from '@/components/common/SIMPLE_TOTAL_USER.vue';
import USAGE_RANK_CPU from '@/components/common/USAGE_RANK_CPU.vue';
import USAGE_RANK_GPU from '@/components/common/USAGE_RANK_GPU.vue';
import USAGE_RANK_MEM from '@/components/common/USAGE_RANK_MEM.vue';
import USAGE_RANK_IDLE from '@/components/common/USAGE_RANK_IDLE.vue';
import SIMPLE_GPU_DETAILS from '@/components/common/SIMPLE_GPU_DETAILS.vue';

const selectedStartDate = ref('2025-01-01');
const selectedEndDate = ref('2025-01-03');
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