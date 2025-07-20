<template>
  <div class="home-container">
    <div class="container-fluid p-4">
      <div class="row">
        <!-- 左侧：任务创建表单 -->
        <div class="col-lg-4 mb-4">
          <div class="modern-card p-4">
            <h3 class="card-title mb-4">
              <i class="fas fa-plus-circle me-2"></i>
              创建爬虫任务
            </h3>
            
            <el-form 
              :model="formData" 
              label-width="100px" 
              label-position="top"
              @submit.prevent="submitTask"
            >
              <!-- 平台选择 -->
              <el-form-item label="目标平台">
                <!-- 当前选择平台显示卡片 -->
                <div v-if="formData.platform" class="selected-platform-card mt-3">
                  <div class="platform-card-header">
                    <i :class="getSelectedPlatformIcon()" class="platform-icon"></i>
                    <div class="platform-info">
                      <div class="platform-name">{{ getSelectedPlatformName() }}</div>
                      <div class="platform-status">当前选择的爬取平台</div>
                    </div>
                    <div class="platform-badge">
                      <i class="fas fa-check-circle"></i>
                    </div>
                  </div>
                </div>

                <div class="d-flex gap-2">
                  <el-select v-model="formData.platform" placeholder="选择平台" style="flex: 1">
                    <el-option 
                      v-for="platform in PLATFORMS" 
                      :key="platform.value" 
                      :label="platform.label" 
                      :value="platform.value"
                    >
                      <i :class="platform.icon" class="me-2"></i>
                      {{ platform.label }}
                    </el-option>
                  </el-select>
                  <el-button 
                    type="info" 
                    @click="showPlatformExample" 
                    :disabled="!formData.platform"
                    size="default"
                  >
                    <i class="fas fa-info-circle"></i>
                  </el-button>
                </div>
                
                
              </el-form-item>

              <!-- 登录类型 -->
              <el-form-item label="登录方式">
                <el-select v-model="formData.lt" placeholder="选择登录方式" style="width: 100%">
                  <el-option 
                    v-for="type in LOGIN_TYPES" 
                    :key="type.value" 
                    :label="type.label" 
                    :value="type.value"
                  />
                </el-select>
              </el-form-item>

              <!-- 爬虫类型 -->
              <el-form-item label="爬虫类型">
                <el-select v-model="formData.type" placeholder="选择爬虫类型" style="width: 100%">
                  <el-option 
                    v-for="type in CRAWLER_TYPES" 
                    :key="type.value" 
                    :label="type.label" 
                    :value="type.value"
                  />
                </el-select>
              </el-form-item>

              <!-- 搜索关键词 -->
              <el-form-item label="搜索关键词" v-if="formData.type === 'search'">
                <el-input 
                  v-model="formData.keywords" 
                  :placeholder="getKeywordsPlaceholder()"
                  clearable
                />
              </el-form-item>

              <!-- 动态输入栏 -->
              <el-form-item 
                v-for="field in getDynamicFields()" 
                :key="field.key" 
                :label="field.label"
              >
                <el-input 
                  v-if="field.type === 'input'"
                  v-model="formData[field.key]" 
                  :placeholder="field.placeholder"
                  clearable
                />
                <el-input 
                  v-else-if="field.type === 'textarea'"
                  v-model="formData[field.key]" 
                  type="textarea"
                  :rows="3"
                  :placeholder="field.placeholder"
                />
              </el-form-item>

              <!-- 起始页数 -->
              <el-form-item label="起始页数">
                <div class="d-flex gap-2">
                  <el-input-number 
                    v-model="formData.start" 
                    :min="1" 
                    :max="100" 
                    placeholder="起始页数"
                    style="flex: 1"
                  />
                  <el-button 
                    type="info" 
                    @click="showStartPageTip" 
                    size="default"
                    class="start-page-tip-btn"
                  >
                    <i class="fas fa-info-circle"></i>
                  </el-button>
                </div>
                <div class="text-muted small mt-1">
                  （仅在搜索类型中生效，用于控制分页爬取的起始位置）
                </div>
              </el-form-item>

              <!-- 爬取数量限制 -->
              <el-form-item label="爬取数量">
                <el-input-number 
                  v-model="formData.max_count" 
                  :min="1" 
                  :max="1000" 
                  placeholder="最大爬取数量"
                  style="width: 100%"
                />
                <div class="text-muted small mt-1">
                  （设置爬取的最大帖子/视频数量，避免无限爬取）
                </div>
              </el-form-item>

              <!-- 评论设置 -->
              <el-form-item label="评论抓取">
                <div class="d-flex flex-column gap-2">
                  <el-checkbox v-model="formData.get_comment">抓取一级评论</el-checkbox>
                  <el-checkbox v-model="formData.get_sub_comment" :disabled="!formData.get_comment">
                    抓取二级评论
                  </el-checkbox>
                </div>
              </el-form-item>

              <!-- MySQL同步保存选项 -->
              <el-form-item label="数据保存">
                <el-checkbox v-model="formData.sync_to_mysql">
                  同步保存至MySQL数据库中
                </el-checkbox>
                <div class="text-muted small mt-1">
                  （数据默认保存在SQLite数据库中，勾选此项将同时保存到MySQL数据库）
                </div>
              </el-form-item>

              <!-- Cookies -->
              <el-form-item label="Cookies" v-if="formData.lt === 'cookie'">
                <el-input 
                  v-model="formData.cookies" 
                  type="textarea" 
                  :rows="3" 
                  placeholder="请输入cookies字符串"
                />
              </el-form-item>

              <!-- 提交按钮 -->
              <el-form-item>
                <div class="d-flex gap-2 w-100">
                  <!--<el-button 
                    type="primary" 
                    @click="submitTask('sync')"
                    :loading="loading.submit"
                    style="flex: 1"
                  >
                    <i class="fas fa-play me-1"></i>
                    同步执行
                  </el-button>-->
                  <el-button 
                    type="success" 
                    @click="submitTask('async')"
                    :loading="loading.submit"
                    style="flex: 1"
                  >
                    <i class="fas fa-rocket me-1"></i>
                    执行任务（异步）
                  </el-button>
                </div>
              </el-form-item>

              <!-- 重置按钮 -->
              <el-form-item>
                <el-button @click="resetForm" style="width: 100%" plain>
                  <i class="fas fa-undo me-1"></i>
                  重置表单
                </el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>

        <!-- 右侧：任务列表和统计 -->
        <div class="col-lg-8">
          <!-- 任务统计卡片 -->
          <div class="row mb-4">
            <div class="col-md-3 mb-3">
              <div class="stat-card modern-card p-3 text-center">
                <div class="stat-icon total">
                  <i class="fas fa-tasks"></i>
                </div>
                <div class="stat-number">{{ taskStats.total }}</div>
                <div class="stat-label">总任务数</div>
              </div>
            </div>
            <div class="col-md-3 mb-3">
              <div class="stat-card modern-card p-3 text-center">
                <div class="stat-icon running">
                  <i class="fas fa-spinner fa-spin"></i>
                </div>
                <div class="stat-number">{{ taskStats.running }}</div>
                <div class="stat-label">运行中</div>
              </div>
            </div>
            <div class="col-md-3 mb-3">
              <div class="stat-card modern-card p-3 text-center">
                <div class="stat-icon completed">
                  <i class="fas fa-check-circle"></i>
                </div>
                <div class="stat-number">{{ taskStats.completed }}</div>
                <div class="stat-label">已完成</div>
              </div>
            </div>
            <div class="col-md-3 mb-3">
              <div class="stat-card modern-card p-3 text-center">
                <div class="stat-icon failed">
                  <i class="fas fa-exclamation-circle"></i>
                </div>
                <div class="stat-number">{{ taskStats.failed }}</div>
                <div class="stat-label">失败</div>
              </div>
            </div>
          </div>

          <!-- 任务列表 -->
          <div class="modern-card p-4">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h3 class="card-title mb-0">
                <i class="fas fa-list me-2"></i>
                任务列表
              </h3>
              <el-button 
                type="primary" 
                :icon="Refresh" 
                @click="getAllTasks"
                :loading="loading.tasks"
                size="small"
              >
                刷新
              </el-button>
            </div>

            <div v-if="loading.tasks" class="text-center py-4">
              <el-loading-spinner size="large" />
              <p class="mt-2 text-muted">加载任务列表...</p>
            </div>

            <div v-else-if="tasks.length === 0" class="text-center py-5">
              <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
              <p class="text-muted">暂无任务记录</p>
            </div>

            <div v-else class="task-list">
              <div 
                v-for="task in tasks" 
                :key="task.task_times_id" 
                class="task-item modern-card p-3 mb-3"
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
                    <div class="d-flex gap-2 justify-content-end">
                      <!-- 查看详情 -->
                      <el-button 
                          type="info" 
                          size="small" 
                          @click="showTaskDetail(task)"
                          circle
                        >
                          <i class="fas fa-eye"></i>
                        </el-button>
                      
                      <!-- 刷新状态 -->
                      <el-button 
                        v-if="task.status === 'running'" 
                        type="primary" 
                        size="small" 
                        @click="refreshTaskStatus(task.task_times_id)"
                        circle
                      >
                        <i class="fas fa-sync-alt"></i>
                      </el-button>
                      
                      <!-- 删除任务 -->
                      <el-button 
                        type="danger" 
                        size="small" 
                        @click="deleteTask(task.task_times_id)"
                        circle
                      >
                        <i class="fas fa-trash"></i>
                      </el-button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 任务详情对话框 -->
    <TaskDetailDialog 
      v-model="showDetailDialog" 
      :task="selectedTask" 
      @refresh="refreshTaskStatus"
    />

    <!-- 同步任务结果对话框 -->
    <SyncResultDialog 
      v-model="showSyncResult" 
      :result="syncResult" 
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import { useCrawlerStore } from '../stores/crawler'
import { PLATFORMS, LOGIN_TYPES, CRAWLER_TYPES, PLATFORM_EXAMPLES } from '../api'
import SystemStatus from '../components/SystemStatus.vue'
import TaskDetailDialog from '../components/TaskDetailDialog.vue'
import SyncResultDialog from '../components/SyncResultDialog.vue'

// Store
const crawlerStore = useCrawlerStore()

// 响应式数据
const showDetailDialog = ref(false)
const selectedTask = ref(null)
const showSyncResult = ref(false)
const syncResult = ref(null)
const refreshTimer = ref(null)
const systemStatusRef = ref(null)

// 计算属性
const formData = computed(() => crawlerStore.formData)
const tasks = computed(() => crawlerStore.tasks)
const currentTask = computed(() => crawlerStore.currentTask)
const systemStatus = computed(() => crawlerStore.systemStatus)
const loading = computed(() => crawlerStore.loading)
const taskStats = computed(() => crawlerStore.taskStats)

// 确保formData包含动态字段
if (!formData.value.detail_urls) {
  formData.value.detail_urls = ''
}
if (!formData.value.creator_ids) {
  formData.value.creator_ids = ''
}

// 系统状态样式
const systemStatusClass = computed(() => {
  switch (systemStatus.value.status) {
    case 'healthy': return 'status-completed'
    case 'error': return 'status-failed'
    default: return 'status-running'
  }
})

// 方法
const submitTask = async (mode) => {
  try {
    // 验证表单
    if (formData.value.type === 'search' && !formData.value.keywords) {
      ElMessage.warning('搜索类型需要输入关键词')
      return
    }
    
    if (formData.value.type === 'detail' && !formData.value.detail_urls) {
      ElMessage.warning('详情页模式需要输入详情页参数')
      return
    }
    
    if (formData.value.type === 'creator' && !formData.value.creator_ids) {
      ElMessage.warning('创作者模式需要输入创作者参数')
      return
    }
    
    // Cookie登录的cookies字段设置为非必填项
    // if (formData.value.lt === 'cookie' && !formData.value.cookies) {
    //   ElMessage.warning('Cookie登录需要输入cookies')
    //   return
    // }

    // 准备提交数据，处理动态字段
    const submitData = { ...formData.value }
    
    // 移除前端特有的字段
    delete submitData.detail_urls
    delete submitData.creator_ids
    
    // 根据爬虫类型处理动态字段
    if (formData.value.type === 'detail' && formData.value.detail_urls) {
      // 将换行分隔的URL转换为数组
      const ids = formData.value.detail_urls.split('\n').filter(url => url.trim()).map(url => url.trim())
      if (ids.length > 0) {
        submitData.specified_ids = ids
      }
    } else if (formData.value.type === 'creator' && formData.value.creator_ids) {
      // 将换行分隔的ID转换为数组
      const ids = formData.value.creator_ids.split('\n').filter(id => id.trim()).map(id => id.trim())
      if (ids.length > 0) {
        submitData.creator_ids = ids
      }
    }

    if (mode === 'sync') {
      // 同步执行
      const result = await crawlerStore.submitSyncTask(submitData)
      syncResult.value = result
      showSyncResult.value = true
      ElMessage.success('任务执行完成')
    } else {
      // 异步执行
      const task = await crawlerStore.submitAsyncTask(submitData)
      const taskIdDisplay = task.task_times_id ? task.task_times_id.substring(0, 8) : '未知'
      ElMessage.success(`任务已提交，任务ID: ${taskIdDisplay}...`)
    }
  } catch (error) {
    ElMessage.error(error.message || '提交任务失败')
  }
}

const resetForm = () => {
  crawlerStore.resetForm()
  ElMessage.success('表单已重置')
}

const getAllTasks = async () => {
  await crawlerStore.getAllTasks()
}

const refreshTaskStatus = async (taskId) => {
  if (!taskId || taskId === 'undefined') {
    ElMessage.error('无效的任务ID')
    return
  }
  try {
    await crawlerStore.getTaskStatus(taskId)
    ElMessage.success('状态已更新')
  } catch (error) {
    ElMessage.error('更新状态失败')
  }
}

const deleteTask = async (taskId) => {
  if (!taskId || taskId === 'undefined') {
    ElMessage.error('无效的任务ID')
    return
  }
  try {
    await ElMessageBox.confirm(
      '确定要删除这个任务吗？',
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await crawlerStore.deleteTask(taskId)
    ElMessage.success('任务已删除')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除任务失败')
    }
  }
}

const showTaskDetail = (task) => {
  selectedTask.value = task
  showDetailDialog.value = true
}

const refreshData = async () => {
  await Promise.all([
    crawlerStore.getSystemStatus(),
    crawlerStore.getAllTasks()
  ])
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

const formatTime = (timeStr) => {
  if (!timeStr) return ''
  return new Date(timeStr).toLocaleString('zh-CN')
}

const showPlatformExample = () => {
  const platform = formData.value.platform
  const example = PLATFORM_EXAMPLES[platform]
  
  if (example) {
    const platformName = PLATFORMS.find(p => p.value === platform)?.label || platform
    
    let content = `<div style="text-align: left;">
      <h4>${platformName} 格式说明</h4>`
    
    // 详情页格式
    if (example.detail && example.detail.examples.length > 0) {
      content += `
        <div style="margin-bottom: 15px;">
          <p><strong>${example.detail.title}：</strong></p>
          <p style="color: #666; font-size: 12px;">${example.detail.description}</p>
          <div style="background: #f5f5f5; padding: 8px; border-radius: 4px; font-family: monospace; font-size: 12px;">
            ${example.detail.examples.map(ex => `<div style="margin: 2px 0;">${ex}</div>`).join('')}
          </div>
        </div>`
    }
    
    // 创作者格式
    if (example.creator && example.creator.examples.length > 0) {
      content += `
        <div style="margin-bottom: 15px;">
          <p><strong>${example.creator.title}：</strong></p>
          <p style="color: #666; font-size: 12px;">${example.creator.description}</p>
          <div style="background: #f5f5f5; padding: 8px; border-radius: 4px; font-family: monospace; font-size: 12px;">
            ${example.creator.examples.map(ex => `<div style="margin: 2px 0;">${ex}</div>`).join('')}
          </div>
        </div>`
    }
    
    content += `</div>`
    
    ElMessageBox.alert(
      content,
      '平台格式提示',
      {
        dangerouslyUseHTMLString: true,
        confirmButtonText: '知道了'
      }
    )
  }
}

const showStartPageTip = () => {
  const content = `<div style="text-align: left; max-height: 500px; overflow-y: auto;">
    <p><strong>注："起始页数"仅在搜索类型中生效，用于控制分页爬取的起始位置</strong></p>
    <h4>📋 起始页参数说明</h4>
    <div style="margin-bottom: 15px;">
      <p><strong>参数定义：</strong></p>
      <ul style="margin: 8px 0; padding-left: 20px; color: #666;">
        <li>参数名称：--start (命令行) / START_PAGE (配置)</li>
        <li>默认值：1（在 base_config.py 第74行定义）</li>
        <li>作用范围：仅在 search 类型的爬取中生效</li>
      </ul>
    </div>
    
    <div style="margin-bottom: 15px;">
      <p><strong>✅ 支持起始页参数的平台：</strong></p>
      <div style="background: #f8f9fa; padding: 12px; border-radius: 6px; margin: 8px 0;">
        <div style="margin-bottom: 8px;"><strong>🔴 小红书 (XHS)</strong></div>
        <div style="font-size: 12px; color: #666; margin-left: 15px;">
          📍 实现位置：core.py 第126行<br>
          🔄 分页逻辑：while (page - start_page + 1) * xhs_limit_count <= config.CRAWLER_MAX_NOTES_COUNT<br>
          📄 每页固定：20条内容
        </div>
      </div>
      
      <div style="background: #f8f9fa; padding: 12px; border-radius: 6px; margin: 8px 0;">
        <div style="margin-bottom: 8px;"><strong>🎵 抖音 (DouYin)</strong></div>
        <div style="font-size: 12px; color: #666; margin-left: 15px;">
          📍 实现位置：core.py 第104行<br>
          🔄 分页逻辑：while (page - start_page + 1) * dy_limit_count <= config.CRAWLER_MAX_NOTES_COUNT<br>
          📄 每页固定：10条内容
        </div>
      </div>
      
      <div style="background: #f8f9fa; padding: 12px; border-radius: 6px; margin: 8px 0;">
        <div style="margin-bottom: 8px;"><strong>⚡ 快手 (KuaiShou)</strong></div>
        <div style="font-size: 12px; color: #666; margin-left: 15px;">
          📍 实现位置：core.py 第110行<br>
          🔄 分页逻辑：类似其他平台的实现<br>
          📄 每页固定：20条内容
        </div>
      </div>
      
      <div style="background: #f8f9fa; padding: 12px; border-radius: 6px; margin: 8px 0;">
        <div style="margin-bottom: 8px;"><strong>📺 B站 (Bilibili)</strong></div>
        <div style="font-size: 12px; color: #666; margin-left: 15px;">
          📍 实现位置：core.py 第153行<br>
          🔄 分页逻辑：start_page = config.START_PAGE<br>
          📄 每页固定：20条内容
        </div>
      </div>
      
      <div style="background: #f8f9fa; padding: 12px; border-radius: 6px; margin: 8px 0;">
        <div style="margin-bottom: 8px;"><strong>🐦 微博 (Weibo)</strong></div>
        <div style="font-size: 12px; color: #666; margin-left: 15px;">
          📍 实现位置：core.py 第126行<br>
          🔄 分页逻辑：while (page - start_page + 1) * weibo_limit_count <= config.CRAWLER_MAX_NOTES_COUNT<br>
          📄 每页固定：10条内容
        </div>
      </div>
      
      <div style="background: #f8f9fa; padding: 12px; border-radius: 6px; margin: 8px 0;">
        <div style="margin-bottom: 8px;"><strong>🤔 知乎 (Zhihu)</strong></div>
        <div style="font-size: 12px; color: #666; margin-left: 15px;">
          📍 实现位置：core.py 第130行<br>
          🔄 分页逻辑：start_page = config.START_PAGE<br>
          📄 每页固定：20条内容
        </div>
      </div>
      
      <div style="background: #f8f9fa; padding: 12px; border-radius: 6px; margin: 8px 0;">
        <div style="margin-bottom: 8px;"><strong>💬 贴吧 (Tieba)</strong></div>
        <div style="font-size: 12px; color: #666; margin-left: 15px;">
          📍 实现位置：core.py<br>
          🔄 分页逻辑：支持起始页设置
        </div>
      </div>
    </div>
    
    <div style="margin-bottom: 15px;">
      <p><strong>🚫 不支持起始页参数的情况：</strong></p>
      <ul style="margin: 8px 0; padding-left: 20px; color: #666;">
        <li><strong>detail 类型</strong>：获取指定帖子详情，无分页概念</li>
        <li><strong>creator 类型</strong>：获取创作者主页数据，通常从第一页开始获取所有内容</li>
      </ul>
    </div>
    
    <div style="margin-bottom: 15px;">
      <p><strong>💡 实际应用场景：</strong></p>
      <ul style="margin: 8px 0; padding-left: 20px; color: #666;">
        <li><strong>断点续爬</strong>：当爬取中断时，可以从指定页数继续</li>
        <li><strong>分段爬取</strong>：将大量数据分段处理，避免单次爬取时间过长</li>
        <li><strong>跳过已爬取内容</strong>：避免重复爬取前面的页面</li>
        <li><strong>测试特定页面</strong>：针对特定页面进行测试和调试</li>
      </ul>
    </div>
    
    <div style="margin-bottom: 15px;">
      <p><strong>⚙️ 使用示例：</strong></p>
      <div style="background: #f5f5f5; padding: 12px; border-radius: 6px; font-family: monospace; font-size: 12px;">
        <div style="margin: 4px 0; color: #28a745;"># 从第5页开始爬取小红书内容</div>
        <div style="margin: 4px 0;">python main.py --platform xhs --type search --start 5 --keywords "编程"</div>
        <div style="margin: 8px 0; color: #28a745;"># 从第3页开始爬取抖音内容</div>
        <div style="margin: 4px 0;">python main.py --platform dy --type search --start 3 --keywords "技术分享"</div>
      </div>
    </div>
  </div>`
  
  ElMessageBox.alert(
    content,
    '起始页参数详细说明',
    {
      dangerouslyUseHTMLString: true,
      confirmButtonText: '知道了',
      customStyle: {
        width: '600px'
      }
    }
  )
}

const getKeywordsPlaceholder = () => {
  const type = formData.value.type
  if (type === 'search') {
    return '请输入搜索关键词'
  } else if (type === 'detail') {
    return '详情页爬取模式下此字段无效'
  } else if (type === 'creator') {
    return '创作者主页模式下此字段无效'
  }
  return '请输入搜索关键词'
}

const getDynamicFields = () => {
  const type = formData.value.type
  const platform = formData.value.platform
  const fields = []
  
  if (type === 'detail') {
    fields.push({
      key: 'detail_urls',
      label: '详情页参数(ID/URL)',
      type: 'textarea',
      placeholder: platform ? getDetailPlaceholder(platform) : '请先选择平台，然后点击右侧提示按钮查看格式说明\n多个ID/URL请用换行分隔'
    })
  } else if (type === 'creator') {
    fields.push({
      key: 'creator_ids',
      label: '创作者参数(ID/URL)',
      type: 'textarea', 
      placeholder: platform ? getCreatorPlaceholder(platform) : '请先选择平台，然后点击右侧提示按钮查看格式说明\n多个ID/URL请用换行分隔'
    })
  }
  
  return fields
}

const getDetailPlaceholder = (platform) => {
  const example = PLATFORM_EXAMPLES[platform]
  if (example && example.detail && example.detail.examples.length > 0) {
    return `${example.detail.description}\n\n示例：\n${example.detail.examples.slice(0, 2).join('\n')}\n\n多个ID/URL请用换行分隔`
  }
  return '请输入详情页ID或URL，多个请用换行分隔'
}

const getCreatorPlaceholder = (platform) => {
  const example = PLATFORM_EXAMPLES[platform]
  if (example && example.creator && example.creator.examples.length > 0) {
    return `${example.creator.description}\n\n示例：\n${example.creator.examples.slice(0, 2).join('\n')}\n\n多个ID/URL请用换行分隔`
  }
  return '请输入创作者ID或URL，多个请用换行分隔'
}

// 获取当前选择平台的图标
const getSelectedPlatformIcon = () => {
  if (!formData.value.platform) return ''
  const platform = PLATFORMS.find(p => p.value === formData.value.platform)
  return platform ? platform.icon : ''
}

// 获取当前选择平台的名称
const getSelectedPlatformName = () => {
  if (!formData.value.platform) return ''
  const platform = PLATFORMS.find(p => p.value === formData.value.platform)
  return platform ? platform.label : ''
}

// 生命周期
onMounted(async () => {
  // 初始化数据
  await refreshData()
  
  // 设置定时刷新运行中的任务
  refreshTimer.value = setInterval(() => {
    crawlerStore.refreshRunningTasks()
  }, 10000) // 每10秒刷新一次
})

onUnmounted(() => {
  if (refreshTimer.value) {
    clearInterval(refreshTimer.value)
  }
})
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px 0;
}

.status-bar {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 15px 0;
  margin: 0 20px;
}

.page-title {
  color: white;
  font-weight: 600;
  margin: 0;
  font-size: 1.8rem;
}

.card-title {
  color: #333;
  font-weight: 600;
  font-size: 1.2rem;
}

/* 平台选择区域样式 */
.d-flex {
  display: flex;
}

.gap-2 {
  gap: 8px;
}

.me-2 {
  margin-right: 8px;
}

/* 动态字段样式 */
.dynamic-field {
  margin-bottom: 16px;
}

.dynamic-field .el-textarea__inner {
  min-height: 80px;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.4;
}

.dynamic-field .el-input__inner {
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
}

/* 提示按钮样式 */
.platform-tip-btn {
  min-width: 40px;
  padding: 8px 12px;
}

.platform-tip-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.start-page-tip-btn {
  min-width: 40px;
  padding: 8px 12px;
  transition: all 0.3s ease;
}

.start-page-tip-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

/* 选择平台显示卡片样式 */
.selected-platform-card {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border: 2px solid #e3f2fd;
  border-radius: 12px;
  padding: 16px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.selected-platform-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  border-color: #2196f3;
}

.platform-card-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.platform-icon {
  font-size: 24px;
  color: #2196f3;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(33, 150, 243, 0.1);
  border-radius: 50%;
  transition: all 0.3s ease;
}

.selected-platform-card:hover .platform-icon {
  background: rgba(33, 150, 243, 0.2);
  transform: scale(1.1);
}

.platform-info {
  flex: 1;
}

.platform-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 2px;
}

.platform-status {
  font-size: 12px;
  color: #666;
  opacity: 0.8;
}

.platform-badge {
  color: #4caf50;
  font-size: 18px;
  animation: pulse-check 2s infinite;
}

@keyframes pulse-check {
  0% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.1);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

.stat-card {
  transition: all 0.3s ease;
  border: none;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 10px;
  font-size: 1.5rem;
  color: white;
}

.stat-icon.total {
  background: linear-gradient(45deg, #667eea, #764ba2);
}

.stat-icon.running {
  background: linear-gradient(45deg, #ff6b35, #f7931e);
}

.stat-icon.completed {
  background: linear-gradient(45deg, #28a745, #20c997);
}

.stat-icon.failed {
  background: linear-gradient(45deg, #dc3545, #e83e8c);
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.stat-label {
  color: #666;
  font-size: 0.9rem;
}

.task-item {
  border: 1px solid rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.task-item:hover {
  transform: translateX(5px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.task-title {
  font-weight: 500;
  color: #333;
  margin-bottom: 4px;
}

.task-meta {
  font-size: 0.85rem;
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

@media (max-width: 768px) {
  .home-container {
    padding: 10px 0;
  }
  
  .status-bar {
    margin: 0 10px;
  }
  
  .page-title {
    font-size: 1.4rem;
  }
  
  .stat-number {
    font-size: 1.5rem;
  }
  
  /* 响应式设计 */
  .d-flex {
    flex-direction: column;
  }
  
  .gap-2 {
    gap: 8px;
  }
  
  .platform-tip-btn {
    width: 100%;
    margin-top: 8px;
  }
}
</style>