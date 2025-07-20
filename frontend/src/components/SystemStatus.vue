<template>
  <div class="system-status">
    <div class="status-card" :class="statusClass">
      <div class="status-header">
        <div class="status-icon">
          <i :class="statusIcon"></i>
        </div>
        <div class="status-info">
          <h4 class="status-title">{{ statusText }}</h4>
          <p class="status-subtitle">{{ statusSubtitle }}</p>
        </div>
        <div class="status-actions">
          <el-button 
            type="text" 
            size="small" 
            @click="checkStatus"
            :loading="checking"
            class="refresh-btn"
          >
            <i class="fas fa-sync-alt"></i>
          </el-button>
        </div>
      </div>
      
      <div class="status-details" v-if="showDetails">
        <div class="detail-item">
          <label>API地址:</label>
          <span class="api-url">{{ apiUrl }}</span>
        </div>
        <div class="detail-item" v-if="lastCheck">
          <label>最后检查:</label>
          <span>{{ formatTime(lastCheck) }}</span>
        </div>
        <div class="detail-item" v-if="responseTime">
          <label>响应时间:</label>
          <span class="response-time">{{ responseTime }}ms</span>
        </div>
        <div class="detail-item" v-if="errorMessage">
          <label>错误信息:</label>
          <span class="error-message">{{ errorMessage }}</span>
        </div>
      </div>
      
      <div class="status-footer">
        <el-button 
          type="text" 
          size="small" 
          @click="toggleDetails"
          class="toggle-btn"
        >
          {{ showDetails ? '收起详情' : '查看详情' }}
          <i :class="showDetails ? 'fas fa-chevron-up' : 'fas fa-chevron-down'" class="ms-1"></i>
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { systemAPI } from '../api'

// Props
const props = defineProps({
  autoRefresh: {
    type: Boolean,
    default: true
  },
  refreshInterval: {
    type: Number,
    default: 30000 // 30秒
  }
})

// 响应式数据
const status = ref('checking') // checking, online, offline, error
const checking = ref(false)
const showDetails = ref(false)
const lastCheck = ref(null)
const responseTime = ref(null)
const errorMessage = ref('')
const apiUrl = ref('http://localhost:8000')

// 定时器
let refreshTimer = null

// 计算属性
const statusClass = computed(() => {
  switch (status.value) {
    case 'online': return 'status-online'
    case 'offline': return 'status-offline'
    case 'error': return 'status-error'
    default: return 'status-checking'
  }
})

const statusIcon = computed(() => {
  switch (status.value) {
    case 'online': return 'fas fa-check-circle'
    case 'offline': return 'fas fa-times-circle'
    case 'error': return 'fas fa-exclamation-triangle'
    default: return 'fas fa-spinner fa-spin'
  }
})

const statusText = computed(() => {
  switch (status.value) {
    case 'online': return 'API服务正常'
    case 'offline': return 'API服务离线'
    case 'error': return 'API服务异常'
    default: return '检查中...'
  }
})

const statusSubtitle = computed(() => {
  switch (status.value) {
    case 'online': return '所有功能可正常使用'
    case 'offline': return '无法连接到API服务'
    case 'error': return '服务响应异常'
    default: return '正在检查服务状态'
  }
})

// 方法
const checkStatus = async () => {
  if (checking.value) return
  
  checking.value = true
  const startTime = Date.now()
  
  try {
    const response = await systemAPI.getHealth()
    const endTime = Date.now()
    
    responseTime.value = endTime - startTime
    lastCheck.value = new Date()
    errorMessage.value = ''
    
    if (response.status === 'healthy') {
      status.value = 'online'
    } else {
      status.value = 'error'
      errorMessage.value = response.message || '服务状态异常'
    }
  } catch (error) {
    const endTime = Date.now()
    responseTime.value = endTime - startTime
    lastCheck.value = new Date()
    status.value = 'offline'
    errorMessage.value = error.message || '连接失败'
    
    console.error('Health check failed:', error)
  } finally {
    checking.value = false
  }
}

const toggleDetails = () => {
  showDetails.value = !showDetails.value
}

const formatTime = (date) => {
  if (!date) return ''
  return date.toLocaleString('zh-CN')
}

const startAutoRefresh = () => {
  if (!props.autoRefresh) return
  
  refreshTimer = setInterval(() => {
    checkStatus()
  }, props.refreshInterval)
}

const stopAutoRefresh = () => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
}

// 生命周期
onMounted(() => {
  checkStatus()
  startAutoRefresh()
})

onUnmounted(() => {
  stopAutoRefresh()
})

// 暴露方法给父组件
defineExpose({
  checkStatus,
  status: computed(() => status.value)
})
</script>

<style scoped>
.system-status {
  width: 100%;
}

.status-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.status-card.status-online {
  border-color: #52c41a;
  background: linear-gradient(135deg, #f6ffed 0%, #ffffff 100%);
}

.status-card.status-offline {
  border-color: #ff4d4f;
  background: linear-gradient(135deg, #fff2f0 0%, #ffffff 100%);
}

.status-card.status-error {
  border-color: #faad14;
  background: linear-gradient(135deg, #fffbe6 0%, #ffffff 100%);
}

.status-card.status-checking {
  border-color: #1890ff;
  background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%);
}

.status-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: white;
}

.status-online .status-icon {
  background: #52c41a;
}

.status-offline .status-icon {
  background: #ff4d4f;
}

.status-error .status-icon {
  background: #faad14;
}

.status-checking .status-icon {
  background: #1890ff;
}

.status-info {
  flex: 1;
}

.status-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #262626;
}

.status-subtitle {
  margin: 4px 0 0 0;
  font-size: 14px;
  color: #8c8c8c;
}

.status-actions {
  display: flex;
  align-items: center;
}

.refresh-btn {
  color: #8c8c8c;
  padding: 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.refresh-btn:hover {
  color: #1890ff;
  background: rgba(24, 144, 255, 0.1);
}

.status-details {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.detail-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  gap: 8px;
}

.detail-item:last-child {
  margin-bottom: 0;
}

.detail-item label {
  font-weight: 500;
  color: #595959;
  min-width: 80px;
  margin: 0;
  font-size: 14px;
}

.api-url {
  font-family: 'Courier New', monospace;
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
  color: #1890ff;
}

.response-time {
  color: #52c41a;
  font-weight: 500;
  font-size: 14px;
}

.error-message {
  color: #ff4d4f;
  font-size: 14px;
  word-break: break-word;
}

.status-footer {
  margin-top: 12px;
  text-align: center;
}

.toggle-btn {
  color: #8c8c8c;
  font-size: 13px;
  padding: 4px 8px;
  transition: all 0.2s ease;
}

.toggle-btn:hover {
  color: #1890ff;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .status-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .status-actions {
    align-self: flex-end;
  }
  
  .detail-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }
  
  .detail-item label {
    min-width: auto;
  }
}

/* 动画效果 */
.status-card {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 状态指示器动画 */
.status-checking .status-icon i {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>