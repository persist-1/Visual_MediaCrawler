<template>
  <el-dialog
    v-model="visible"
    title="同步任务执行结果"
    width="70%"
    :before-close="handleClose"
    class="sync-result-dialog"
  >
    <div v-if="result" class="result-container">
      <!-- 执行状态 -->
      <div class="status-section mb-4">
        <div class="status-header">
          <div class="status-icon" :class="getStatusClass(result.success)">
            <i :class="getStatusIcon(result.success)"></i>
          </div>
          <div class="status-info">
            <h4 class="status-title">{{ getStatusTitle(result.success) }}</h4>
            <p class="status-message">{{ result.message || '任务执行完成' }}</p>
          </div>
        </div>
      </div>

      <!-- 任务信息 -->
      <div class="info-section mb-4" v-if="result.task_times_id">
        <h5 class="section-title">
          <i class="fas fa-info-circle me-2"></i>
          任务信息
        </h5>
        <div class="info-grid">
          <div class="info-item">
            <label>任务ID:</label>
            <span class="task-id">{{ result.task_times_id }}</span>
            <el-button 
              type="text" 
              size="small" 
              @click="copyToClipboard(result.task_times_id)"
              class="ms-2"
            >
              <i class="fas fa-copy"></i>
            </el-button>
          </div>
          <div class="info-item" v-if="result.execution_time">
            <label>执行时间:</label>
            <span class="execution-time">{{ formatDuration(result.execution_time) }}</span>
          </div>
        </div>
      </div>

      <!-- 数据统计 -->
      <div class="data-section mb-4" v-if="result.data && result.data.length > 0">
        <h5 class="section-title">
          <i class="fas fa-chart-bar me-2"></i>
          数据统计
        </h5>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="fas fa-database"></i>
            </div>
            <div class="stat-info">
              <h6>采集数据</h6>
              <p class="stat-number">{{ result.data.length }}</p>
            </div>
          </div>
          <div class="stat-card" v-if="getUniqueAuthors(result.data).length > 0">
            <div class="stat-icon">
              <i class="fas fa-users"></i>
            </div>
            <div class="stat-info">
              <h6>作者数量</h6>
              <p class="stat-number">{{ getUniqueAuthors(result.data).length }}</p>
            </div>
          </div>
          <div class="stat-card" v-if="getTotalLikes(result.data) > 0">
            <div class="stat-icon">
              <i class="fas fa-heart"></i>
            </div>
            <div class="stat-info">
              <h6>总点赞数</h6>
              <p class="stat-number">{{ formatNumber(getTotalLikes(result.data)) }}</p>
            </div>
          </div>
          <div class="stat-card" v-if="getTotalComments(result.data) > 0">
            <div class="stat-icon">
              <i class="fas fa-comments"></i>
            </div>
            <div class="stat-info">
              <h6>总评论数</h6>
              <p class="stat-number">{{ formatNumber(getTotalComments(result.data)) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 数据预览 -->
      <div class="preview-section mb-4" v-if="result.data && result.data.length > 0">
        <h5 class="section-title">
          <i class="fas fa-eye me-2"></i>
          数据预览
          <span class="preview-count">(前{{ Math.min(5, result.data.length) }}条)</span>
        </h5>
        <div class="data-preview">
          <div 
            v-for="(item, index) in result.data.slice(0, 5)" 
            :key="index"
            class="preview-item"
          >
            <div class="item-header">
              <div class="item-index">{{ index + 1 }}</div>
              <div class="item-meta">
                <span class="author" v-if="item.author">{{ item.author }}</span>
                <span class="date" v-if="item.create_time">{{ formatDate(item.create_time) }}</span>
              </div>
            </div>
            <div class="item-content">
              <p class="content-text">{{ truncateText(item.content || item.title || '无内容', 100) }}</p>
              <div class="item-stats" v-if="item.liked_count || item.comment_count">
                <span v-if="item.liked_count" class="stat-item">
                  <i class="fas fa-heart"></i>
                  {{ formatNumber(item.liked_count) }}
                </span>
                <span v-if="item.comment_count" class="stat-item">
                  <i class="fas fa-comment"></i>
                  {{ formatNumber(item.comment_count) }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 错误信息 -->
      <div class="error-section" v-if="!result.success && result.error">
        <h5 class="section-title error">
          <i class="fas fa-exclamation-triangle me-2"></i>
          错误详情
        </h5>
        <div class="error-content">
          <pre>{{ result.error }}</pre>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button 
          v-if="result?.data && result.data.length > 0" 
          type="primary" 
          @click="exportData"
        >
          <i class="fas fa-download me-1"></i>
          导出数据
        </el-button>
        <el-button @click="handleClose">关闭</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  result: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['update:modelValue'])

// 计算属性
const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 方法
const handleClose = () => {
  visible.value = false
}

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    ElMessage.success('已复制到剪贴板')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

const exportData = () => {
  if (!props.result?.data) return
  
  try {
    const dataStr = JSON.stringify(props.result.data, null, 2)
    const blob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    
    const link = document.createElement('a')
    link.href = url
    link.download = `crawler_data_${new Date().getTime()}.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    URL.revokeObjectURL(url)
    ElMessage.success('数据导出成功')
  } catch (error) {
    ElMessage.error('数据导出失败')
  }
}

// 工具函数
const getStatusClass = (success) => {
  return success ? 'status-success' : 'status-error'
}

const getStatusIcon = (success) => {
  return success ? 'fas fa-check-circle' : 'fas fa-times-circle'
}

const getStatusTitle = (success) => {
  return success ? '执行成功' : '执行失败'
}

const formatDuration = (seconds) => {
  if (!seconds) return ''
  if (seconds < 60) return `${seconds.toFixed(1)}秒`
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = (seconds % 60).toFixed(1)
  return `${minutes}分${remainingSeconds}秒`
}

const formatNumber = (num) => {
  if (!num) return '0'
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万'
  }
  return num.toLocaleString()
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString('zh-CN')
}

const truncateText = (text, maxLength) => {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

const getUniqueAuthors = (data) => {
  if (!data || !Array.isArray(data)) return []
  const authors = data.map(item => item.author).filter(Boolean)
  return [...new Set(authors)]
}

const getTotalLikes = (data) => {
  if (!data || !Array.isArray(data)) return 0
  return data.reduce((total, item) => total + (parseInt(item.liked_count) || 0), 0)
}

const getTotalComments = (data) => {
  if (!data || !Array.isArray(data)) return 0
  return data.reduce((total, item) => total + (parseInt(item.comment_count) || 0), 0)
}
</script>

<style scoped>
.sync-result-dialog {
  --el-dialog-border-radius: 16px;
}

.result-container {
  max-height: 70vh;
  overflow-y: auto;
}

.status-section {
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #e9ecef;
}

.status-header {
  display: flex;
  align-items: center;
  gap: 15px;
}

.status-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.status-icon.status-success {
  background: linear-gradient(135deg, #52c41a, #73d13d);
}

.status-icon.status-error {
  background: linear-gradient(135deg, #ff4d4f, #ff7875);
}

.status-info {
  flex: 1;
}

.status-title {
  margin: 0 0 5px 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #262626;
}

.status-message {
  margin: 0;
  color: #8c8c8c;
  font-size: 0.95rem;
}

.info-section,
.data-section,
.preview-section,
.error-section {
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

.section-title.error {
  color: #dc3545;
}

.preview-count {
  font-size: 0.9rem;
  color: #8c8c8c;
  font-weight: normal;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 15px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: white;
  border-radius: 8px;
  border: 1px solid #dee2e6;
}

.info-item label {
  font-weight: 500;
  color: #6c757d;
  min-width: 80px;
  margin: 0;
}

.task-id {
  font-family: 'Courier New', monospace;
  background: #e9ecef;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9rem;
}

.execution-time {
  color: #1890ff;
  font-weight: 500;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #dee2e6;
  display: flex;
  align-items: center;
  gap: 15px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
}

.stat-info h6 {
  margin: 0 0 5px 0;
  font-size: 0.9rem;
  color: #8c8c8c;
  font-weight: 500;
}

.stat-number {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #262626;
}

.data-preview {
  background: white;
  border-radius: 8px;
  border: 1px solid #dee2e6;
  overflow: hidden;
}

.preview-item {
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
}

.preview-item:last-child {
  border-bottom: none;
}

.item-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.item-index {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #1890ff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: 600;
}

.item-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
}

.author {
  font-weight: 500;
  color: #262626;
}

.date {
  color: #8c8c8c;
  font-size: 0.9rem;
}

.content-text {
  margin: 0 0 10px 0;
  line-height: 1.5;
  color: #595959;
}

.item-stats {
  display: flex;
  gap: 15px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #8c8c8c;
  font-size: 0.9rem;
}

.stat-item i {
  color: #ff4d4f;
}

.error-content {
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

.error-content pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* 滚动条样式 */
.result-container::-webkit-scrollbar,
.error-content::-webkit-scrollbar {
  width: 6px;
}

.result-container::-webkit-scrollbar-track,
.error-content::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.result-container::-webkit-scrollbar-thumb,
.error-content::-webkit-scrollbar-thumb {
  background: rgba(102, 126, 234, 0.3);
  border-radius: 3px;
}

.result-container::-webkit-scrollbar-thumb:hover,
.error-content::-webkit-scrollbar-thumb:hover {
  background: rgba(102, 126, 234, 0.5);
}

@media (max-width: 768px) {
  .stats-grid,
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .status-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .item-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
}
</style>