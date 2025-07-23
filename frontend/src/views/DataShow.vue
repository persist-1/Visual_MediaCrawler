<template>
  <div class="data-show-container">
    <div class="container-fluid p-4">
      <!-- 数据源选择 -->
      <div class="modern-card p-4 mb-4">
        <div class="row align-items-center">
          <div class="col-md-12">
            <label class="form-label mb-2">
              <i class="fas fa-database me-1"></i>
              数据源选择
            </label>
            <el-radio-group v-model="selectedDataSource" @change="onDataSourceChange" class="data-source-group">
              <el-radio value="sqlite" class="data-source-option">
                <i class="fas fa-file-alt me-2"></i>
                查询SQLite数据库
              </el-radio>
              <el-radio value="mysql" class="data-source-option">
                <i class="fas fa-database me-2"></i>
                查询MySQL数据库
              </el-radio>
            </el-radio-group>
          </div>
        </div>
      </div>

      <!-- 数据表选择和控制 -->
      <div class="modern-card p-4 mb-4">
        <div class="row align-items-center mb-3">
          <div class="col-md-6">
            <label class="form-label mb-2">数据表选择</label>
            <el-select 
              v-model="selectedTable" 
              placeholder="选择数据表" 
              @change="onTableChange"
              style="width: 100%"
            >
              <el-option 
                v-for="table in availableTables" 
                :key="table.value" 
                :label="table.label" 
                :value="table.value"
              >
                <i :class="table.icon" class="me-2"></i>
                {{ table.label }}
              </el-option>
            </el-select>
          </div>
          <div class="col-md-6">
            <label class="form-label mb-2">每页显示</label>
            <el-select 
              v-model="pageSize" 
              @change="onPageSizeChange"
              style="width: 100%"
            >
              <el-option label="30条/页" :value="30" />
              <el-option label="60条/页" :value="60" />
              <el-option label="100条/页" :value="100" />
            </el-select>
          </div>
        </div>
        <div class="row align-items-center">
          <div class="col-md-8">
            <!-- 当前筛选状态显示 -->
            <div v-if="taskIdFilter" class="filter-status">
              <span class="badge bg-primary me-2">
                <i class="fas fa-filter me-1"></i>
                筛选中: 任务ID {{ taskIdFilter.substring(0, 8) }}...
              </span>
              <el-button size="small" type="info" @click="clearTaskFilter" plain>
                <i class="fas fa-times me-1"></i>
                清除筛选
              </el-button>
            </div>
          </div>
          <div class="col-md-4 text-end">
            <el-dropdown @command="handleExportCommand" :disabled="!selectedTable || tableData.length === 0">
              <el-button 
                type="success" 
                :disabled="!selectedTable || tableData.length === 0"
              >
                <i class="fas fa-download me-1"></i>
                导出数据
                <el-icon class="el-icon--right"><arrow-down /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="csv">
                    <i class="fas fa-file-csv me-2"></i>
                    导出为CSV
                  </el-dropdown-item>
                  <el-dropdown-item command="json">
                    <i class="fas fa-file-code me-2"></i>
                    导出为JSON
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </div>

      <!-- 筛选功能区块 -->
      <div class="modern-card p-4 mb-4">
        <div class="row align-items-center">
          <div class="col-md-12">
            <label class="form-label mb-2">
              <i class="fas fa-filter me-1"></i>
              数据筛选
            </label>
            <div class="d-flex gap-2">
              <el-input
                v-model="taskIdFilter"
                placeholder="输入任务ID或选择任务"
                clearable
                @clear="clearTaskFilter"
                @input="onTaskIdInput"
                style="flex: 1"
              >
                <template #suffix>
                  <el-button
                    type="primary"
                    size="small"
                    @click="showTaskSelector"
                    style="border: none; background: none; color: #409eff;"
                  >
                    <i class="fas fa-list"></i>
                  </el-button>
                </template>
              </el-input>
            </div>
          </div>
        </div>
      </div>

      <!-- 数据表格 -->
      <div class="modern-card p-4">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h3 class="card-title mb-0">
            <i class="fas fa-table me-2"></i>
            {{ getTableDisplayName(selectedTable) }}
          </h3>
          <div class="text-muted">
            共 {{ totalCount }} 条数据
          </div>
        </div>

        <div v-if="loading" class="text-center py-4">
          <el-loading-spinner size="large" />
          <p class="mt-2 text-muted">加载数据中...</p>
        </div>

        <div v-else-if="!selectedTable" class="text-center py-5">
          <i class="fas fa-table fa-3x text-muted mb-3"></i>
          <p class="text-muted">请选择要查看的数据表</p>
        </div>

        <div v-else-if="tableData.length === 0" class="text-center py-5">
          <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
          <p class="text-muted">暂无数据</p>
        </div>

        <div v-else>
          <!-- 动态表格 -->
          <el-table 
            :data="tableData" 
            stripe 
            border
            style="width: 100%"
            max-height="600"
          >
            <el-table-column 
              v-for="column in tableColumns" 
              :key="column.prop"
              :prop="column.prop"
              :label="column.label"
              :width="column.width"
              :min-width="column.minWidth"
              :formatter="column.formatter"
              show-overflow-tooltip
            />
          </el-table>

          <!-- 分页 -->
          <div class="pagination-container mt-4">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :page-sizes="[30, 60, 100]"
              :total="totalCount"
              :layout="paginationLayout"
              :small="isMobile"
              @size-change="onPageSizeChange"
              @current-change="onPageChange"
              class="responsive-pagination"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- 任务选择对话框 -->
    <el-dialog
      v-model="showTaskSelectorDialog"
      title="选择爬取任务"
      width="80%"
      class="task-selector-dialog"
    >
      <div class="task-selector-content">
        <div v-if="loadingTasks" class="text-center py-4">
          <el-loading-spinner size="large" />
          <p class="mt-2 text-muted">加载任务列表...</p>
        </div>
        
        <div v-else-if="availableTasks.length === 0" class="text-center py-5">
          <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
          <p class="text-muted">暂无任务记录</p>
        </div>
        
        <div v-else class="task-list">
          <div 
            v-for="task in availableTasks" 
            :key="task.task_times_id" 
            class="task-card modern-card p-3 mb-3"
            @click="selectTask(task)"
          >
            <div class="row align-items-center">
              <div class="col-md-8">
                <div class="d-flex align-items-center gap-3">
                  <!-- 状态指示器 -->
                  <div class="status-indicator" :class="getTaskStatusClass(task.status)">
                    <div class="status-dot"></div>
                    {{ getTaskStatusText(task.status) }}
                  </div>
                  
                  <!-- 任务信息 -->
                  <div>
                    <div class="task-title">
                      <i :class="getPlatformIcon(task.formData?.platform)" class="me-1"></i>
                      {{ getPlatformName(task.formData?.platform) }} - 
                      {{ getCrawlerTypeName(task.formData?.type) }}
                    </div>
                    <div class="task-meta text-muted small">
                      <span v-if="task.formData?.keywords">
                        关键词: {{ task.formData.keywords }} | 
                      </span>
                      <span>任务ID: {{ task.task_times_id.substring(0, 8) }}... | </span>
                      <span>创建时间: {{ formatTime(task.created_at) }}</span>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="col-md-4 text-end">
                <el-button type="primary" size="small">
                  <i class="fas fa-check me-1"></i>
                  选择此任务
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh, ArrowDown } from '@element-plus/icons-vue'
import { useDataStore } from '../stores/data'
import { useCrawlerStore } from '../stores/crawler'
import { PLATFORMS, CRAWLER_TYPES } from '../api'

// Store
const dataStore = useDataStore()
const crawlerStore = useCrawlerStore()

// 响应式数据
const selectedDataSource = ref('sqlite')
const selectedTable = ref('')
const currentPage = ref(1)
const pageSize = ref(30)
const taskIdFilter = ref('')
const showTaskSelectorDialog = ref(false)
const availableTasks = ref([])
const loadingTasks = ref(false)

// 移动端检测
const isMobile = ref(false)
const isTablet = ref(false)

// 检测屏幕尺寸
const checkScreenSize = () => {
  const width = window.innerWidth
  isMobile.value = width <= 768
  isTablet.value = width > 768 && width <= 1024
}

// 监听窗口大小变化
const handleResize = () => {
  checkScreenSize()
}

// 响应式分页布局
const paginationLayout = computed(() => {
  if (isMobile.value) {
    return 'prev, pager, next'
  } else if (isTablet.value) {
    return 'total, prev, pager, next'
  } else {
    return 'total, sizes, prev, pager, next, jumper'
  }
})

// 计算属性
const loading = computed(() => dataStore.loading)
const tableData = computed(() => dataStore.tableData)
const totalCount = computed(() => dataStore.totalCount)
const tableColumns = computed(() => dataStore.tableColumns)
const availableTables = computed(() => dataStore.availableTables)

// 方法
const refreshData = async () => {
  if (selectedTable.value) {
    await loadTableData()
  }
}

const onTableChange = async () => {
  currentPage.value = 1
  await loadTableData()
}

const onPageChange = async () => {
  await loadTableData()
}

const onPageSizeChange = async () => {
  currentPage.value = 1
  await loadTableData()
}

const loadTableData = async () => {
  if (!selectedTable.value) return
  
  try {
    await dataStore.loadTableData({
      table: selectedTable.value,
      page: currentPage.value,
      pageSize: pageSize.value,
      taskId: taskIdFilter.value || undefined,
      dataSource: selectedDataSource.value
    })
  } catch (error) {
    ElMessage.error('加载数据失败: ' + error.message)
  }
}

// 数据源切换方法
const onDataSourceChange = async () => {
  // 清空当前选择的表格
  selectedTable.value = ''
  // 重新加载可用表格列表
  await dataStore.loadAvailableTables(selectedDataSource.value)
  // 清空当前数据
  dataStore.clearTableData()
  ElMessage.success(`已切换到${selectedDataSource.value === 'sqlite' ? 'SQLite' : 'MySQL'}数据源`)
}

// 处理导出命令
const handleExportCommand = (command) => {
  exportData(command)
}

// 导出数据
const exportData = async (format = 'csv') => {
  if (!selectedTable.value) {
    ElMessage.warning('请先选择数据表')
    return
  }
  
  try {
    if (format === 'csv') {
      await dataStore.exportTableData(selectedTable.value, taskIdFilter.value, selectedDataSource.value)
      ElMessage.success('CSV数据导出成功')
    } else if (format === 'json') {
      await dataStore.exportTableDataAsJSON(selectedTable.value, taskIdFilter.value, selectedDataSource.value)
      ElMessage.success('JSON数据导出成功')
    }
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败: ' + error.message)
  }
}

const getTableDisplayName = (tableName) => {
  const table = availableTables.value.find(t => t.value === tableName)
  return table ? table.label : tableName
}

const formatTime = (timeStr) => {
  if (!timeStr) return '--'
  return new Date(timeStr).toLocaleString('zh-CN')
}

// 任务筛选相关方法
const showTaskSelector = async () => {
  loadingTasks.value = true
  showTaskSelectorDialog.value = true
  
  try {
    // 根据当前选择的数据源获取对应的任务列表
    await crawlerStore.getAllTasks(selectedDataSource.value)
    availableTasks.value = crawlerStore.tasks
  } catch (error) {
    ElMessage.error('加载任务列表失败: ' + error.message)
  } finally {
    loadingTasks.value = false
  }
}

const selectTask = (task) => {
  taskIdFilter.value = task.task_times_id
  showTaskSelectorDialog.value = false
  // 重新加载数据
  if (selectedTable.value) {
    currentPage.value = 1
    loadTableData()
  }
  ElMessage.success(`已选择任务: ${task.task_times_id.substring(0, 8)}...`)
}

const clearTaskFilter = () => {
  taskIdFilter.value = ''
  // 重新加载数据
  if (selectedTable.value) {
    currentPage.value = 1
    loadTableData()
  }
}

// 防抖定时器
let debounceTimer = null

const onTaskIdInput = () => {
  // 清除之前的定时器
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
  
  // 设置新的定时器，500ms后执行搜索
  debounceTimer = setTimeout(() => {
    if (selectedTable.value) {
      currentPage.value = 1
      loadTableData()
    }
  }, 500)
}

// 任务状态相关方法
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

// 生命周期
onMounted(async () => {
  // 初始化屏幕尺寸检测
  checkScreenSize()
  window.addEventListener('resize', handleResize)
  
  await dataStore.loadAvailableTables(selectedDataSource.value)
})

// 页面卸载时清理事件监听器
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

// 监听表格选择变化
watch(selectedTable, (newTable) => {
  if (newTable) {
    loadTableData()
  }
})

// 导出方法到模板
defineExpose({
  handleExportCommand,
  exportData,
  refreshData,
  loadTableData,
  showTaskSelector,
  selectTask,
  clearTaskFilter,
  onTaskIdInput,
  onDataSourceChange,
  getTableDisplayName,
  formatTime,
  getTaskStatusClass,
  getTaskStatusText,
  getPlatformIcon,
  getPlatformName,
  getCrawlerTypeName
})
</script>

<style scoped>
/* 数据源选择样式 */
.data-source-group {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.data-source-option {
  padding: 12px 16px;
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  transition: all 0.3s ease;
  background: #fff;
  min-width: 200px;
}

.data-source-option:hover {
  border-color: #409eff;
  background: #f0f9ff;
}

.data-source-option.is-checked {
  border-color: #409eff;
  background: #e6f7ff;
  color: #409eff;
}

/* 筛选状态样式 */
.filter-status {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-status .badge {
  font-size: 0.875rem;
  padding: 6px 12px;
}

/* 任务选择对话框样式 */
.task-selector-dialog .el-dialog__body {
  padding: 20px;
  max-height: 60vh;
  overflow-y: auto;
}

.task-card {
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e4e7ed;
}

.task-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #409eff;
}

.task-title {
  font-weight: 500;
  color: #333;
  margin-bottom: 4px;
}

.task-meta {
  font-size: 0.85rem;
}

/* 状态指示器样式 */
.status-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
  min-width: 70px;
  justify-content: center;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
}

.status-running {
  background: rgba(255, 193, 7, 0.1);
  color: #ffc107;
  border: 1px solid rgba(255, 193, 7, 0.3);
}

.status-running .status-dot {
  animation: pulse 2s infinite;
}

.status-completed {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
  border: 1px solid rgba(40, 167, 69, 0.3);
}

.status-failed {
  background: rgba(220, 53, 69, 0.1);
  color: #dc3545;
  border: 1px solid rgba(220, 53, 69, 0.3);
}

@keyframes pulse {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
  100% {
    opacity: 1;
  }
}
.data-show-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f48fb1 0%, #ff8a65 15%, #ffffff 25%, #ffffff 70%, #f8b5a0 85%, #ffb4cd 100%); /** 数据展示页面容器组件背景 */
}

.status-bar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem 0;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.page-title {
  font-size: 1.8rem;
  font-weight: 600;
  margin: 0;
}

.modern-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  border: none;
  transition: all 0.3s ease;
}

.modern-card:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.card-title {
  color: #2c3e50;
  font-weight: 600;
  font-size: 1.2rem;
}

:deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.el-table th) {
  background-color: #f8f9fa;
  color: #2c3e50;
  font-weight: 600;
}

:deep(.el-pagination) {
  justify-content: center;
}

/* 分页容器响应式样式 */
.pagination-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.responsive-pagination {
  width: 100%;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

/* 移动端分页样式优化 */
@media (max-width: 768px) {
  .pagination-container {
    padding: 1rem 0;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 8px;
    margin: 1rem 0;
  }
  
  :deep(.el-pagination) {
    justify-content: center;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  
  :deep(.el-pagination .el-pager) {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.25rem;
  }
  
  :deep(.el-pagination .el-pager li) {
    min-width: 32px;
    height: 32px;
    line-height: 30px;
    font-size: 14px;
    margin: 0 2px;
  }
  
  :deep(.el-pagination .btn-prev),
  :deep(.el-pagination .btn-next) {
    min-width: 32px;
    height: 32px;
    line-height: 30px;
    font-size: 14px;
  }
  
  :deep(.el-pagination .el-pagination__total) {
    font-size: 12px;
    margin-right: 8px;
  }
  
  :deep(.el-pagination .el-pagination__sizes) {
    margin: 0 8px;
  }
  
  :deep(.el-pagination .el-pagination__jump) {
    margin-left: 8px;
    font-size: 12px;
  }
}

/* 平板端分页样式 */
@media (max-width: 1024px) and (min-width: 769px) {
  .pagination-container {
    padding: 0.75rem 0;
  }
  
  :deep(.el-pagination .el-pager li) {
    min-width: 36px;
    height: 36px;
    line-height: 34px;
  }
  
  :deep(.el-pagination .btn-prev),
  :deep(.el-pagination .btn-next) {
    min-width: 36px;
    height: 36px;
    line-height: 34px;
  }
}

/* 小屏幕手机端优化 */
@media (max-width: 480px) {
  .pagination-container {
    padding: 0.5rem;
    margin: 0.5rem 0;
  }
  
  :deep(.el-pagination) {
    font-size: 12px;
  }
  
  :deep(.el-pagination .el-pager li) {
    min-width: 28px;
    height: 28px;
    line-height: 26px;
    font-size: 12px;
    margin: 0 1px;
  }
  
  :deep(.el-pagination .btn-prev),
  :deep(.el-pagination .btn-next) {
    min-width: 28px;
    height: 28px;
    line-height: 26px;
    font-size: 12px;
  }
  
  :deep(.el-pagination .el-pagination__total) {
    display: none; /* 在极小屏幕上隐藏总数显示 */
  }
}
</style>