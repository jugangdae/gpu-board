<!-- src/components/reports/SystemInfoCards.vue -->
<template>
  <v-row class="mb-6">
    <v-col cols="12" md="3">
      <v-card color="deep-purple lighten-2" class="pa-4 text-white" style="border:1.5px solid #e0e0e0;">
        <div class="d-flex align-center mb-1">
          <v-icon size="32">mdi-account-multiple</v-icon>
          <span class="text-h6 ml-2">총 유저</span>
        </div>
        <div class="d-flex align-center">
          <div class="text-h3 font-weight-bold">{{ sysinfo.user_count }}</div>
        </div>
      </v-card>
    </v-col>
    <v-col cols="12" md="3">
      <v-card color="indigo darken-1" class="pa-4 text-white" style="border:1.5px solid #e0e0e0;">
        <div class="d-flex align-center mb-1">
          <v-icon size="32">mdi-nvidia</v-icon>
          <span class="text-h6 ml-2">GPU</span>
        </div>
        <div class="text-h3 font-weight-bold">{{ sysinfo.gpu_count }}</div>
        <div class="text-caption mt-1">모델: {{ sysinfo.gpu_models?.join(', ') }}</div>
        <div class="text-caption">사용중: {{ sysinfo.gpu_used }}/{{ sysinfo.gpu_count }}</div>
      </v-card>
    </v-col>
    <v-col cols="12" md="3">
      <v-card color="cyan darken-2" class="pa-4 text-white" style="border:1.5px solid #e0e0e0;">
        <div class="d-flex align-center mb-1">
          <v-icon size="32">mdi-chip</v-icon>
          <span class="text-h6 ml-2">CPU</span>
        </div>
        <div class="text-h3 font-weight-bold">{{ sysinfo.cpu_count }}</div>
        <div class="text-caption mt-1">모델: {{ sysinfo.cpu_models?.join(', ') }}</div>
        <div class="text-caption">사용중: {{ sysinfo.cpu_used }}/{{ sysinfo.cpu_count }}</div>
      </v-card>
    </v-col>
    <v-col cols="12" md="3">
      <v-card color="green darken-1" class="pa-4 text-white" style="border:1.5px solid #e0e0e0;">
        <div class="d-flex align-center mb-1">
          <v-icon size="32">mdi-memory</v-icon>
          <span class="text-h6 ml-2">메모리</span>
        </div>
        <div class="text-h3 font-weight-bold">{{ sysinfo.memory_total_tb }}TB</div>
        <div class="text-caption mt-1">슬롯: {{ sysinfo.memory_count }}개</div>
        <div class="text-caption">사용중: {{ sysinfo.memory_used }}/{{ sysinfo.memory_count }}</div>
      </v-card>
    </v-col>
  </v-row>
</template>
<script setup>
defineProps({
  sysinfo: { type: Object, required: true }
})
</script>
