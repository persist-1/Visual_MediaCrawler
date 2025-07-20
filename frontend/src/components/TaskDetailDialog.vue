<template>
  <el-dialog
    v-model="visible"
    title="任务详情"
    width="80%"
    :before-close="handleClose"
    class="task-detail-dialog"
  >
    <div v-if="currentTask" class="task-detail-content">
      <!-- 任务基本信息 -->
      <div class="info-section mb-4">
        <h4 class="section-title">
          <i class="fas fa-info-circle me-2"></i>
          基本信息
        </h4>
        <div class="row">
          <div class="col-md-6">
            <div class="info-item">
              <label>任务ID:</label>
              <span class="task-id">{{ currentTask.task_times_id }}</span>
              <el-button 
                type="text" 
                size="small" 
                @click="copyToClipboard(currentTask.task_times_id)"
                class="ms-2"
              >
                <i class="fas fa-copy"></i>
              </el-button>
            </div>
            <div class="info-item">
              <label>状态:</label>
              <div class="status-indicator" :class="getTaskStatusClass(currentTask.status)">
                <div class="status-dot"></div>
                {{ getTaskStatusText(currentTask.status) }}
              </div>
            </div>
            <div class="info-item">
              <label>创建时间:</label>
              <span>{{ formatTime(currentTask.created_at) }}</span>
            </div>
            <div class="info-item" v-if="currentTask.updated_at">
              <label>更新时间:</label>
              <span>{{ formatTime(currentTask.updated_at) }}</span>
            </div>
          </div>
          <div class="col-md-6">
            <div class="info-item" v-if="currentTask.formData">
              <label>目标平台:</label>
              <span>
                <i :class="getPlatformIcon(currentTask.formData.platform)" class="me-1"></i>
                {{ getPlatformName(currentTask.formData.platform) }}
              </span>
            </div>
            <div class="info-item" v-if="currentTask.formData">
              <label>爬虫类型:</label>
              <span>{{ getCrawlerTypeName(currentTask.formData.type) }}</span>
            </div>
            <div class="info-item" v-if="currentTask.formData?.keywords">
              <label>搜索关键词:</label>
              <span class="keyword-tag">{{ currentTask.formData.keywords }}</span>
            </div>
            <div class="info-item" v-if="currentTask.formData">
              <label>登录方式:</label>
              <span>{{ getLoginTypeName(currentTask.formData.lt) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 任务配置 -->
      <div class="info-section mb-4" v-if="currentTask.formData">
        <h4 class="section-title">
          <i class="fas fa-cog me-2"></i>
          任务配置
        </h4>
        <div class="config-grid">
          <div class="config-item" v-if="currentTask.formData.start">
            <label>起始页数:</label>
            <span>{{ currentTask.formData.start }}</span>
          </div>
          <div class="config-item">
            <label>抓取一级评论:</label>
            <span class="boolean-value" :class="{ active: currentTask.formData.get_comment }">
              {{ currentTask.formData.get_comment ? '是' : '否' }}
            </span>
          </div>
          <div class="config-item">
            <label>抓取二级评论:</label>
            <span class="boolean-value" :class="{ active: currentTask.formData.get_sub_comment }">
              {{ currentTask.formData.get_sub_comment ? '是' : '否' }}
            </span>
          </div>
          <div class="config-item">
            <label>保存格式:</label>
            <span class="save-format">{{ getSaveOptionName(currentTask.formData.save_data_option) }}</span>
          </div>
        </div>
      </div>

      <!-- 执行结果 -->
      <div class="info-section mb-4" v-if="currentTask.result">
        <h4 class="section-title">
          <i class="fas fa-terminal me-2"></i>
          执行结果
        </h4>
        
        <!-- 标准输出 -->
        <div v-if="currentTask.result.stdout" class="result-section">
          <h5 class="result-title">
            <i class="fas fa-file-alt me-2"></i>
            标准输出
          </h5>
          <div class="result-content stdout">
            <pre>{{ currentTask.result.stdout }}</pre>
          </div>
        </div>
        
        <!-- 日志输出 -->
        <div v-if="currentTask.result.stderr" class="result-section mt-3">
          <h5 :class="isActualError ? 'result-title error' : 'result-title info'">
            <i :class="isActualError ? 'fas fa-exclamation-triangle me-2' : 'fas fa-info-circle me-2'"></i>
            {{ isActualError ? '含有错误输出（别紧张，不一定是真的错误O_o）' : '日志输出' }}
          </h5>
          <div :class="isActualError ? 'result-content stderr' : 'result-content logs'">
            <pre>{{ currentTask.result.stderr }}</pre>
          </div>
        </div>
      </div>

      <!-- 任务消息 -->
      <div class="info-section" v-if="currentTask.message">
        <h4 class="section-title">
          <i class="fas fa-comment me-2"></i>
          任务消息
        </h4>
        <div class="message-content">
          {{ currentTask.message }}
        </div>
      </div>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button 
          v-if="currentTask?.status === 'running'" 
          type="primary" 
          @click="refreshStatus"
          :loading="refreshing"
        >
          <i class="fas fa-sync-alt me-1"></i>
          刷新状态
        </el-button>
        <el-button @click="handleClose">关闭</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useCrawlerStore } from '../stores/crawler'
import { PLATFORMS, LOGIN_TYPES, CRAWLER_TYPES, SAVE_OPTIONS } from '../api'

// Store
const crawlerStore = useCrawlerStore()

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  task: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'refresh'])

// 响应式数据
const refreshing = ref(false)

// 计算属性
const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 获取最新的任务状态
const currentTask = computed(() => {
  if (!props.task) return null
  // 从store中获取最新的任务状态
  const latestTask = crawlerStore.tasks.find(t => t.task_times_id === props.task.task_times_id)
  return latestTask || props.task
})

// 判断stderr内容是否为真正的错误
const isActualError = computed(() => {
  if (!currentTask.value?.result?.stderr) return false
  
  const stderr = currentTask.value.result.stderr.toLowerCase()
  
  // 检查是否包含真正的错误关键词
  const errorKeywords = [
    'error:', 'exception:', 'traceback', 'critical:', 
    'failed:', 'fatal:', 'panic:', 'abort:', 
    'segmentation fault', 'core dumped'
  ]
  
  // 如果包含错误关键词，则认为是真正的错误
  const hasErrorKeywords = errorKeywords.some(keyword => stderr.includes(keyword))
  
  // 如果只包含INFO、DEBUG、WARNING级别的日志，则不认为是错误
  const onlyInfoLogs = /^\s*\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\s+\w+\s+(INFO|DEBUG|WARNING)/.test(stderr)
  
  return hasErrorKeywords && !onlyInfoLogs
})

// 方法
const handleClose = () => {
  visible.value = false
}

const refreshStatus = async () => {
  if (!currentTask.value) return
  
  refreshing.value = true
  try {
    emit('refresh', currentTask.value.task_times_id)
    ElMessage.success('状态已刷新')
  } catch (error) {
    ElMessage.error('刷新状态失败')
  } finally {
    refreshing.value = false
  }
}

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    ElMessage.success('已复制到剪贴板')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

// 工具函数
const getTaskStatusClass = (status) => {
  switch (status) {
    case 'running': return 'status-running'
    case 'completed': return 'status-completed'
    case 'failed': return 'status-failed'
    default: return 'status-running'
  }
}

const getTaskStatusText = (status) => {
  switch (status) {
    case 'running': return '运行中'
    case 'completed': return '已完成'
    case 'failed': return '失败'
    default: return '未知'
  }
}

const getPlatformIcon = (platform) => {
  const platformObj = PLATFORMS.find(p => p.value === platform)
  return platformObj?.icon || 'fas fa-globe'
}

const getPlatformName = (platform) => {
  const platformObj = PLATFORMS.find(p => p.value === platform)
  return platformObj?.label || platform
}

const getCrawlerTypeName = (type) => {
  const typeObj = CRAWLER_TYPES.find(t => t.value === type)
  return typeObj?.label || type
}

const getLoginTypeName = (type) => {
  const typeObj = LOGIN_TYPES.find(t => t.value === type)
  return typeObj?.label || type
}

const getSaveOptionName = (option) => {
  const optionObj = SAVE_OPTIONS.find(o => o.value === option)
  return optionObj?.label || option
}

const formatTime = (timeStr) => {
  if (!timeStr) return ''
  return new Date(timeStr).toLocaleString('zh-CN')
}
</script>

<style scoped>
.task-detail-dialog {
  --el-dialog-border-radius: 16px;
}

.task-detail-content {
  max-height: 70vh;
  overflow-y: auto;
}

.info-section {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #e9ecef;
}

.section-title {
  color: #495057;
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 15px;
  padding-bottom: 8px;
  border-bottom: 2px solid #dee2e6;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  gap: 10px;
}

.info-item label {
  font-weight: 500;
  color: #6c757d;
  min-width: 100px;
  margin: 0;
}

.task-id {
  font-family: 'Courier New', monospace;
  background: #e9ecef;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9rem;
}

.keyword-tag {
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 0.9rem;
  font-weight: 500;
}

.config-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
}

.config-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: white;
  border-radius: 8px;
  border: 1px solid #dee2e6;
}

.config-item label {
  font-weight: 500;
  color: #6c757d;
  min-width: 80px;
  margin: 0;
}

.boolean-value {
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
  background: #dc3545;
  color: white;
}

.boolean-value.active {
  background: #28a745;
}

.save-format {
  background: #17a2b8;
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
}

.result-section {
  margin-bottom: 20px;
}

.result-title {
  color: #495057;
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 10px;
}

.result-title.error {
  color: #dc3545;
}

.result-title.info {
  color: #0d6efd;
}

.result-content {
  background: #2d3748;
  color: #e2e8f0;
  border-radius: 8px;
  padding: 15px;
  max-height: 300px;
  overflow-y: auto;
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  line-height: 1.4;
}

.result-content.stderr {
  background: #742a2a;
  color: #fed7d7;
}

.result-content.logs {
  background: #1e3a8a;
  color: #dbeafe;
}

.result-content pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.message-content {
  background: white;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #dee2e6;
  color: #495057;
  line-height: 1.5;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
}

.status-running .status-dot {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* 滚动条样式 */
.task-detail-content::-webkit-scrollbar,
.result-content::-webkit-scrollbar {
  width: 6px;
}

.task-detail-content::-webkit-scrollbar-track,
.result-content::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.task-detail-content::-webkit-scrollbar-thumb,
.result-content::-webkit-scrollbar-thumb {
  background: rgba(102, 126, 234, 0.3);
  border-radius: 3px;
}

.task-detail-content::-webkit-scrollbar-thumb:hover,
.result-content::-webkit-scrollbar-thumb:hover {
  background: rgba(102, 126, 234, 0.5);
}

@media (max-width: 768px) {
  .config-grid {
    grid-template-columns: 1fr;
  }
  
  .info-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
  
  .info-item label {
    min-width: auto;
  }
}
</style>