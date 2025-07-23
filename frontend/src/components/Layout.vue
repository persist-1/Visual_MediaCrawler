<template>
  <div class="layout-container">
    <!-- 顶部状态栏 -->
    <div class="status-bar mb-4">
      <div class="status-content">
        <div class="status-left">
          <div class="logo-section">
            <h1 class="app-title">Visual_MediaCrawler</h1>
            <span class="app-subtitle">可视化媒体数据采集平台(Based on "MediaCrawler")</span>
          </div>
        </div>
        
        <!-- 菜单栏 -->
        <nav class="navigation-menu">
          <router-link 
            v-for="route in menuRoutes" 
            :key="route.path"
            :to="route.path"
            class="nav-item"
            :class="{ 'active': $route.path === route.path }"
          >
            <i :class="route.icon"></i>
            <span>{{ route.title }}</span>
          </router-link>
        </nav>
        
        <div class="status-right">
          <!-- 条款状态组件 -->
          <TermsStatus />
          
          <!-- API状态指示器 -->
          <div class="status-indicator">
            <div class="status-dot" :class="systemStatus.class"></div>
            <span class="status-text">{{ systemStatus.text }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 主要内容区域 -->
    <div class="main-content">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import TermsStatus from './TermsStatus.vue'
import { useTermsStore } from '@/stores/terms'

const route = useRoute()

// 菜单路由配置
const menuRoutes = [
  {
    path: '/intro',
    title: '项目介绍',
    icon: 'iconfont icon-xiangmujieshao'
  },
  {
    path: '/dashboard/data-crawling',
    title: '数据爬取',
    icon: 'iconfont icon-zhizhu'
  },
  {
    path: '/dashboard/data-show',
    title: '数据展示',
    icon: 'iconfont icon-fengfudeshujuzhanshi'
  }
]

// API服务状态
const apiStatus = ref('checking') // 'healthy', 'error', 'unreachable', 'checking'
let statusCheckInterval = null
let hasServerError = ref(false)

// 检查API健康状态
const checkApiHealth = async () => {
  try {
    const response = await axios.get('/api/health', {
      timeout: 5000 // 5秒超时
    })
    
    if (response.status === 200 && response.data.status === 'healthy') {
      apiStatus.value = hasServerError.value ? 'error' : 'healthy'
    } else {
      apiStatus.value = 'error'
    }
  } catch (error) {
    if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
      apiStatus.value = 'unreachable'
    } else if (error.response && error.response.status >= 500) {
      apiStatus.value = 'error'
      hasServerError.value = true
    } else {
      apiStatus.value = 'unreachable'
    }
  }
}

// 设置axios拦截器来监听5xx错误
const setupAxiosInterceptors = () => {
  axios.interceptors.response.use(
    (response) => {
      // 请求成功，重置服务器错误标志
      if (response.status < 500) {
        hasServerError.value = false
      }
      return response
    },
    (error) => {
      // 检查是否是5xx错误
      if (error.response && error.response.status >= 500) {
        hasServerError.value = true
        apiStatus.value = 'error'
      }
      return Promise.reject(error)
    }
  )
}

// 系统状态计算属性
const systemStatus = computed(() => {
  switch (apiStatus.value) {
    case 'healthy':
      return {
        class: 'online',
        text: 'API服务正常'
      }
    case 'error':
      return {
        class: 'error',
        text: 'API服务异常'
      }
    case 'unreachable':
      return {
        class: 'offline',
        text: 'API服务未连接'
      }
    case 'checking':
    default:
      return {
        class: 'checking',
        text: '检查中...'
      }
  }
})

// 组件挂载时开始检查
onMounted(() => {
  setupAxiosInterceptors()
  checkApiHealth()
  // 每30秒检查一次API状态
  statusCheckInterval = setInterval(checkApiHealth, 30000)
})

// 组件卸载时清理定时器
onUnmounted(() => {
  if (statusCheckInterval) {
    clearInterval(statusCheckInterval)
  }
})
</script>

<style scoped>
.layout-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #ffffff 0%, #ffffff 70%, #ff8a65 85%, #f48fb1 100%); /** /dashboard及其子路由页面的背景 */
  padding: 20px;
}

.status-bar {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 16px 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.status-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.status-left {
  display: flex;
  align-items: center;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.app-title {
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea, #764ba2); /** 项目标题背景 */
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.app-subtitle {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.navigation-menu {
  display: flex;
  gap: 8px;
  background: rgba(255, 255, 255, 0.9); /** 导航菜单背景 */
  padding: 8px;
  border-radius: 12px;
  border: 1px solid rgba(43, 43, 43, 0.2);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 8px;
  text-decoration: none;
  color: #666;
  font-weight: 500;
  font-size: 14px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.nav-item:hover {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  transform: translateY(-1px);
}

.nav-item.active {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.nav-item i {
  font-size: 16px;
  width: 16px;
  text-align: center;
}

.status-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(34, 197, 94, 0.1);
  border-radius: 20px;
  border: 1px solid rgba(34, 197, 94, 0.2);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.status-dot.online {
  background: #22c55e;
}

.status-dot.offline {
  background: #ef4444;
}

.status-dot.error {
  background: #f59e0b;
}

.status-dot.checking {
  background: #6b7280;
}

.status-text {
  font-size: 14px;
  font-weight: 500;
  color: #22c55e;
}

.status-indicator:has(.status-dot.offline) {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.2);
}

.status-indicator:has(.status-dot.offline) .status-text {
  color: #ef4444;
}

.status-indicator:has(.status-dot.error) {
  background: rgba(245, 158, 11, 0.1);
  border-color: rgba(245, 158, 11, 0.2);
}

.status-indicator:has(.status-dot.error) .status-text {
  color: #f59e0b;
}

.status-indicator:has(.status-dot.checking) {
  background: rgba(107, 114, 128, 0.1);
  border-color: rgba(107, 114, 128, 0.2);
}

.status-indicator:has(.status-dot.checking) .status-text {
  color: #6b7280;
}

.main-content {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  min-height: calc(100vh - 140px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  overflow: hidden;
  position: relative;
  z-index: 1;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .status-content {
    flex-direction: column;
    gap: 16px;
  }
  
  .navigation-menu {
    width: 100%;
    justify-content: center;
  }
  
  .nav-item {
    flex: 1;
    justify-content: center;
  }
  
  .app-title {
    font-size: 20px;
  }
  
  .layout-container {
    padding: 12px;
  }
}
</style>