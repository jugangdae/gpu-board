<template>
  <v-container>
    <!-- 자원 검색 (GPU 번호) -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card class="pa-4" style="border:1.5px solid #e0e0e0;">
          <div class="text-h5 mb-2">GPU 자원 검색</div>
          <v-text-field
            v-model="searchKeyword"
            placeholder="GPU 번호 입력 (예: 0, 12)"
            dense
            hide-details
            prepend-inner-icon="mdi-magnify"
            style="max-width: 320px;"
          />
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-btn @click="assignDialog = true" color="primary" class="mb-3">
          <v-icon left>mdi-plus</v-icon> 자원 할당
        </v-btn>
        <router-link to="/reports">
          <v-btn color="info" class="mb-3 ml-3">
            <v-icon left>mdi-chart-bar</v-icon> 자원 현황/보고서 보기
          </v-btn>
        </router-link>
      </v-col>
    </v-row>

    <!-- GPU 자원 테이블 (검색 결과만) -->
    <v-row>
      <v-col cols="12">
        <v-card class="mb-4">
          <v-card-title>
            <span>GPU 자원 목록</span>
          </v-card-title>
          <v-card-text>
            <div v-if="filteredGPUs.length">
              <v-table>
                <thead>
                  <tr>
                    <th>GPU 번호</th>
                    <th>모델</th>
                    <th>사용자</th>
                    <th>기간</th>
                    <th>조치</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="gpu in filteredGPUs" :key="gpu.res_id">
                    <td>{{ gpu.res_id }}</td>
                    <td>{{ gpu.model }}</td>
                    <td>{{ gpu.user || '-' }}</td>
                    <td>
                      <template v-if="gpu.start_date && gpu.end_date">
                        {{ gpu.start_date }} ~ {{ gpu.end_date }}
                      </template>
                      <template v-else>
                        -
                      </template>
                    </td>
                    <td>
                      <v-btn v-if="gpu.user" size="small" color="error" @click="reclaimResource(gpu)">회수</v-btn>
                      <span v-else class="text-grey">-</span>
                    </td>
                  </tr>
                </tbody>
              </v-table>
            </div>
            <div v-else class="text-grey text-caption mt-2">
              해당 GPU 번호의 자원이 없습니다.
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 자원 할당 다이얼로그 (원래와 동일) -->
    <v-dialog v-model="assignDialog" max-width="520">
      <v-card>
        <v-card-title>자원 할당</v-card-title>
        <v-card-text>
          <v-select label="사용자" :items="userNamesList" v-model="assignUser" :rules="[v => !!v || '필수 입력']" dense clearable />
          <v-select label="자원 종류" :items="['GPU', 'CPU', 'Memory']" v-model="assignResourceType" dense />
          <v-select label="자원 선택(복수)" v-model="selectedResourceKeys" :items="filteredAvailableResources"
            item-title="label" item-value="key" multiple :rules="[v => v && v.length > 0 || '최소 1개 선택']" dense />
          <v-menu v-model="menu1" :close-on-content-click="false" transition="scale-transition" offset-y>
            <template #activator="{ props }">
              <v-text-field label="시작일" v-model="startStr" readonly v-bind="props" dense />
            </template>
            <v-date-picker v-model="startObj" @update:model-value="onPickStart" color="primary" />
          </v-menu>
          <v-menu v-model="menu2" :close-on-content-click="false" transition="scale-transition" offset-y>
            <template #activator="{ props }">
              <v-text-field label="만료일" v-model="endStr" readonly v-bind="props" dense />
            </template>
            <v-date-picker v-model="endObj" @update:model-value="onPickEnd" color="primary" />
          </v-menu>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="closeAssignDialog">취소</v-btn>
          <v-btn color="primary" @click="confirmAssign">할당</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

const today = new Date()
const thisYear = today.getFullYear()
const selectedStartDate = ref(`${thisYear}-01-01`)
const selectedEndDate = ref(`${thisYear}-12-31`)
const startDateMenu = ref(false)
const endDateMenu = ref(false)

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

// 사용자/자원 데이터
const users = ref([])
const resources = ref([])

const searchKeyword = ref('')

// GPU만 추출
const gpuResources = computed(() =>
  resources.value.filter(r => r.type === 'GPU')
)

// GPU 번호 검색
const filteredGPUs = computed(() => {
  if (!searchKeyword.value) return gpuResources.value.slice(0, 6)
  const kw = searchKeyword.value.trim()
  // 숫자만 입력된 경우 해당 GPU 번호만
  if (/^\d+$/.test(kw)) {
    return gpuResources.value.filter(gpu => String(gpu.res_id) === kw).slice(0, 6)
  }
  // 일부 텍스트가 들어가면 모델명으로도 검색 가능
  return gpuResources.value.filter(gpu =>
    gpu.model.toLowerCase().includes(kw.toLowerCase())
  ).slice(0, 6)
})

// 할당 관련 데이터 (아래는 원본 유지)
const userNamesList = computed(() => users.value.map(u => typeof u === 'string' ? u : (u.name || String(u))))
const resourceTypeFilter = ref('ALL')
const assignDialog = ref(false)
const assignUser = ref('')
const assignResourceType = ref('GPU')
const selectedResourceKeys = ref([])
const startObj = ref(null)
const endObj = ref(null)
const startStr = ref('')
const endStr = ref('')
const menu1 = ref(false)
const menu2 = ref(false)
const availableResources = computed(() =>
  resources.value
    .filter(r => !r.user)
    .map(r => ({
      key: r.type + '-' + r.res_id,
      label: `${r.type} ${r.res_id}`,
      res_id: r.res_id,
      type: r.type
    }))
)
const filteredAvailableResources = computed(() =>
  availableResources.value.filter(r => r.type === assignResourceType.value)
)
function onPickStart(v) {
  startObj.value = v
  startStr.value = v ? formatDateToString(v) : ''
  menu1.value = false
}
function onPickEnd(v) {
  endObj.value = v
  endStr.value = v ? formatDateToString(v) : ''
  menu2.value = false
}
function closeAssignDialog() {
  assignDialog.value = false
  assignUser.value = ''
  assignResourceType.value = 'GPU'
  selectedResourceKeys.value = []
  startObj.value = null
  endObj.value = null
  startStr.value = ''
  endStr.value = ''
}

async function confirmAssign() {
  if (!assignUser.value || !selectedResourceKeys.value.length || !startStr.value || !endStr.value) {
    alert('모든 값을 입력하세요'); return
  }
  for (const key of selectedResourceKeys.value) {
    const res = availableResources.value.find(r => r.key === key)
    if (!res) continue
    await axios.post('http://localhost:8000/api/allocations', {
      res_id: res.res_id,
      type: res.type,
      user: assignUser.value,
      start_date: startStr.value,
      end_date: endStr.value
    })
  }
  await fetchData()
  closeAssignDialog()
}

async function fetchData() {
  resources.value = (await axios.get('http://localhost:8000/api/resources')).data
  users.value = (await axios.get('http://localhost:8000/api/users')).data
}
fetchData()

async function reclaimResource(r) {
  await axios.post('http://localhost:8000/api/allocations/reclaim', {
    res_id: r.res_id,
    type: r.type
  })
  await fetchData()
}
</script>
