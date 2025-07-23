<template>
  <div class="intro-page">
    <!-- Navigation Bar -->
    <nav class="navbar">
      <div class="nav-container">
        <div class="nav-brand">
          <h2>Visual_MediaCrawler</h2>
        </div>
        
        <!-- 移动端右侧按钮组 -->
        <div class="mobile-nav-actions">
          <!-- GitHub按钮 (仅在移动端显示图标) -->
          <a 
            href="https://github.com/persist-1/Visual_MediaCrawler" 
            target="_blank" 
            class="mobile-github-btn"
          >
            <i class="iconfont icon-GitHub"></i>
          </a>
          
          <!-- 汉堡菜单按钮 (仅在移动端显示) -->
          <button class="mobile-menu-toggle" @click="toggleMobileMenu" :class="{ active: isMobileMenuOpen }">
            <i class="iconfont icon-caidanlan-kucun-kucunchanpinliebiao"></i>
          </button>
        </div>
        
        <!-- 导航链接 -->
        <div class="nav-links" :class="{ 'mobile-open': isMobileMenuOpen }">
          <a href="#features" @click="scrollToSection('features')">主要特性</a>
          <a href="#platforms" @click="scrollToSection('platforms')">支持平台</a>
          <a href="#stats" @click="scrollToSection('stats')">平台数据</a>
          <a href="#docs" @click="scrollToSection('docs')">在线文档</a>
          <a href="#cta" @click="scrollToSection('cta')">立即体验</a>
          <a 
            href="https://github.com/persist-1/Visual_MediaCrawler" 
            target="_blank" 
            class="btn btn-primary desktop-github-btn"
          >
            📖 GitHub
            <span class="github-stars" v-if="githubStars"> ⭐{{ githubStars }}</span>
          </a>
        </div>
      </div>
    </nav>

    <!-- 英雄区域 -->
    <section class="hero">
      <div class="hero-container">
        <div class="hero-badge">🚀 智能媒体数据采集平台</div>
        <h1 class="hero-title">Visual_MediaCrawler</h1>
        <p class="hero-subtitle">
          一个异步、高效、直观的媒体数据采集平台，支持国内主流平台的数据采集，并可导出为 CSV/JSON 格式。
        </p>
        <div class="hero-buttons">
          <button @click="handleDashboardNavigation" class="btn btn-primary btn-large">
            🚀 立即开始
          </button>
          <a href="https://github.com/persist-1/Visual_MediaCrawler" target="_blank" class="btn btn-primary">
           📖 查看源码  <span class="github-stars" v-if="githubStars"> ⭐{{ githubStars }}</span> 
          </a>
        </div>
      </div>
    </section>

    <!-- 功能特色 -->
    <section id="features" class="features">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">主要特性</h2>
          <p class="section-subtitle">
            基于知名开源项目
                <a href="https://github.com/NanmiCoder/MediaCrawler" target="_blank" class="btn btn-primary btn-small">
                MediaCrawler ⭐{{ origin_githubStars }}</a> 
          进行了大幅改动；
          </p>
          <p class="section-subtitle">以"按次"爬取为数据管理理念，专门针对个人爱好者而开发前后端服务，并提供打包程序，在源项目的基础上提供更加便捷的使用方式。</p>
        </div>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h3 class="feature-title">异步高并发</h3>
            <p class="feature-description">
              基于 FastAPI 和 asyncio 实现，提供高性能的数据采集能力，支持大规模并发请求。
            </p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">💾</div>
            <h3 class="feature-title">灵活的数据存储</h3>
            <p class="feature-description">
              默认使用 SQLite 数据库，同时支持 MySQL 存储，提供多种数据导出格式。
            </p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">✨</div>
            <h3 class="feature-title">直观的用户界面</h3>
            <p class="feature-description">
              提供数据爬取和数据展示两个核心界面，操作便捷直观，充分对齐项目核心功能。
            </p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🌐</div>
            <h3 class="feature-title">多平台支持</h3>
            <p class="feature-description">
              支持小红书、抖音、快手、B站、微博、百度贴吧、知乎等主流媒体平台。
            </p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🔧</div>
            <h3 class="feature-title">现代化技术栈</h3>
            <p class="feature-description">
              使用 Python 3.13.5、FastAPI、Vue.js 等现代化技术，确保项目的稳定性和前瞻性。
            </p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3 class="feature-title">数据分析友好</h3>
            <p class="feature-description">
              支持 CSV/JSON 格式导出，便于进行数据分析和提供给 BI 工具使用。
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- 统计数据 -->
    <section id="stats" class="stats">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">平台数据</h2>
          <p class="section-subtitle">
            实时统计数据展示
          </p>
        </div>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-number">12+</div>
            <div class="stat-label">API接口服务</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">20+</div>
            <div class="stat-label">集成的便捷查询数据表</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ githubStars || '2.5k' }}</div>
            <div class="stat-label">GitHub Stars</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">100%</div>
            <div class="stat-label">免费开源</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 支持的平台 -->
    <section id="platforms" class="platforms">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">支持的平台</h2>
          <p class="section-subtitle">
            覆盖国内主流媒体平台，满足不同数据采集需求。
          </p>
        </div>
        <div class="platforms-grid">
          <div class="platform-card">
            <div class="platform-icon"><i class="iconfont icon-xiaohongshu-hui" style="font-size: 36px;"></i></div>
            <h3>小红书</h3>
            <p>搜索、详情页、创作者数据采集</p>
          </div>
          <div class="platform-card">
            <div class="platform-icon"><i class="iconfont icon-douyin" style="font-size: 36px;"></i></div>
            <h3>抖音</h3>
            <p>视频搜索、详情页、创作者数据采集</p>
          </div>
          <div class="platform-card">
            <div class="platform-icon"><i class="iconfont icon-kuaishou" style="font-size: 36px;"></i></div>
            <h3>快手</h3>
            <p>视频搜索、详情页、创作者数据采集</p>
          </div>
          <div class="platform-card">
            <div class="platform-icon"><i class="iconfont icon-bilibili" style="font-size: 36px;"></i></div>
            <h3>哔哩哔哩</h3>
            <p>视频搜索、详情页、UP主数据采集</p>
          </div>
          <div class="platform-card">
            <div class="platform-icon"><i class="iconfont icon-weibo" style="font-size: 36px;"></i></div>
            <h3>微博</h3>
            <p>微博搜索、详情页、用户数据采集</p>
          </div>
          <div class="platform-card">
            <div class="platform-icon"><i class="iconfont icon-social-tieba" style="font-size: 36px;"></i></div>
            <h3>百度贴吧</h3>
            <p>帖子搜索、详情页数据采集</p>
          </div>
          <div class="platform-card">
            <div class="platform-icon"><i class="iconfont icon-zhihu" style="font-size: 36px;"></i></div>
            <h3>知乎</h3>
            <p>问答搜索、详情页、用户数据采集</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 在线文档区域 -->
    <section id="docs" class="docs">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">在线文档</h2>
          <p class="section-subtitle">
            查看详细的项目文档和使用指南
          </p>
        </div>
        <div class="docs-content">
          <div class="docs-grid">
            <!-- WebView 文档预览 -->
            <div class="docs-preview">
              <div class="docs-preview-header">
                <h3>📖 文档预览</h3>
                <a 
                  href="https://persist-1.github.io/Visual_MediaCrawler/" 
                  target="_blank" 
                  class="btn btn-outline btn-small"
                >
                  <i class="fas fa-external-link-alt me-1"></i>
                  在新窗口打开
                </a>
              </div>
              <div class="docs-iframe-container">
                <iframe 
                  src="https://persist-1.github.io/Visual_MediaCrawler/"
                  class="docs-iframe"
                  frameborder="0"
                  loading="lazy"
                ></iframe>
              </div>
            </div>
            
            <!-- 快速链接 -->
            <div class="docs-links">
              <h3>📚 快速导航</h3>
              <div class="docs-link-list">
                <a 
                  href="https://persist-1.github.io/Visual_MediaCrawler/" 
                  target="_blank" 
                  class="docs-link-item"
                >
                  <div class="docs-link-icon">
                    <i class="fas fa-home"></i>
                  </div>
                  <div class="docs-link-content">
                    <h4>项目首页</h4>
                    <p>查看项目概述和特性介绍</p>
                  </div>
                  <i class="fas fa-chevron-right"></i>
                </a>
                
                <a 
                  href="https://persist-1.github.io/Visual_MediaCrawler/" 
                  target="_blank" 
                  class="docs-link-item"
                >
                  <div class="docs-link-icon">
                    <i class="fas fa-rocket"></i>
                  </div>
                  <div class="docs-link-content">
                    <h4>快速开始</h4>
                    <p>了解如何快速部署和使用</p>
                  </div>
                  <i class="fas fa-chevron-right"></i>
                </a>
                
                <a 
                  href="https://persist-1.github.io/Visual_MediaCrawler/" 
                  target="_blank" 
                  class="docs-link-item"
                >
                  <div class="docs-link-icon">
                    <i class="fas fa-cog"></i>
                  </div>
                  <div class="docs-link-content">
                    <h4>配置说明</h4>
                    <p>详细的配置参数和选项</p>
                  </div>
                  <i class="fas fa-chevron-right"></i>
                </a>
                
                <a 
                  href="https://persist-1.github.io/Visual_MediaCrawler/" 
                  target="_blank" 
                  class="docs-link-item"
                >
                  <div class="docs-link-icon">
                    <i class="fas fa-question-circle"></i>
                  </div>
                  <div class="docs-link-content">
                    <h4>常见问题</h4>
                    <p>FAQ 和故障排除指南</p>
                  </div>
                  <i class="fas fa-chevron-right"></i>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA区域 -->
    <section id="cta" class="cta">
      <div class="container">
        <div class="cta-content">
          <h2 class="cta-title">开始您的数据采集之旅</h2>
          <p class="cta-subtitle">
            立即体验 Visual_MediaCrawler，高效采集媒体数据，助力您的数据分析工作。
          </p>
          <button @click="handleDashboardNavigation" class="btn btn-primary btn-large">
            🚀 立即开始
          </button>
        </div>
      </div>
    </section>

    <!-- 条款确认弹窗 -->
    <el-dialog 
      v-model="showTermsDialog" 
      title="使用条款确认" 
      width="60%"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :show-close="false"
    >
      <div class="terms-modal-content">
        <div class="terms-progress">
          <div class="progress-text">
            条款确认进度: {{ currentTermIndex + 1 }} / {{ termsOfUse.length }}
          </div>
          <div class="progress-bar">
            <div 
              class="progress-fill" 
              :style="{ width: ((currentTermIndex + 1) / termsOfUse.length) * 100 + '%' }"
            ></div>
          </div>
        </div>
        
        <div class="current-term" v-if="currentTerm">
          <h3 class="term-title">{{ currentTerm.title }}</h3>
          <div class="term-content">
            {{ currentTerm.content }}
          </div>
        </div>
        
        <el-alert
          title="请仔细阅读并确认上述条款"
          type="warning"
          :closable="false"
          show-icon
        />
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="closeTermsModal">取消</el-button>
          <el-button type="primary" @click="acceptCurrentTerm">
            {{ isLastTerm ? '确认并进入控制台' : '确认此条款' }}
          </el-button>
        </div>
      </template>
    </el-dialog>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useTermsStore } from '@/stores/terms'
import { ElMessage, ElDialog, ElButton, ElAlert } from 'element-plus'

const router = useRouter()
const termsStore = useTermsStore()
const origin_githubStars = ref('')
const githubStars = ref('')

// 条款弹窗相关
const showTermsDialog = ref(false)
const currentTermIndex = ref(0)

// 移动端菜单状态
const isMobileMenuOpen = ref(false)

// 切换移动端菜单
const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

// 关闭移动端菜单
const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}

// 计算属性
const allTermsAccepted = computed(() => termsStore.allTermsAccepted)
const termsOfUse = computed(() => termsStore.termsOfUse)
const currentTerm = computed(() => termsOfUse.value[currentTermIndex.value])
const isLastTerm = computed(() => currentTermIndex.value === termsOfUse.value.length - 1)
// 获取 --源项目-- GitHub Stars数量
const fetchOriginGitHubStars = async () => {
  try {
    const response = await fetch('https://api.github.com/repos/NanmiCoder/MediaCrawler')
    const data = await response.json()
    const stars = data.stargazers_count
    
    // 格式化stars数量
    let formattedStars
    if (stars >= 1000) {
      formattedStars = (stars / 1000).toFixed(1) + 'k'
    } else {
      formattedStars = stars.toString()
    }
    
    origin_githubStars.value = formattedStars
  } catch (error) {
    console.error('无法获取GitHub stars数量:', error)
    // 如果获取失败，使用默认值
    origin_githubStars.value = '2.5k'
  }
}

// 获取 --本项目-- GitHub Stars数量
const fetchGitHubStars = async () => {
  try {
    const response = await fetch('https:///api.github.com/repos/persist-1/Visual_MediaCrawler')
    const data = await response.json()
    const stars = data.stargazers_count
    
    // 格式化stars数量
    let formattedStars
    if (stars >= 1000) {
      formattedStars = (stars / 1000).toFixed(1) + 'k'
    } else {
      formattedStars = stars.toString()
    }
    
    githubStars.value = formattedStars
  } catch (error) {
    console.error('无法获取GitHub stars数量:', error)
    // 如果获取失败，使用默认值
    githubStars.value = '2.5k'
  }
}

// 显示条款弹窗
const showTermsModal = () => {
  currentTermIndex.value = 0
  showTermsDialog.value = true
}

// 接受当前条款
const acceptCurrentTerm = async () => {
  const termId = currentTerm.value.id
  
  // 确认当前条款
  termsStore.acceptTerm(termId)
  
  if (isLastTerm.value) {
    // 所有条款都已确认，关闭弹窗并跳转
    showTermsDialog.value = false
    ElMessage.success('所有条款已确认，正在跳转到控制台...')
    
    // 等待一个tick确保状态更新完成
    await nextTick()
    
    // 直接检查store的状态，不需要额外的更新调用
    if (termsStore.allTermsAccepted) {
      // 短暂延迟后跳转，让用户看到成功消息
      setTimeout(() => {
        router.push('/dashboard/data-crawling')
      }, 800)
    } else {
      ElMessage.error('条款状态更新失败，请重试')
      console.error('条款状态检查失败:', {
        acceptedTerms: termsStore.acceptedTerms,
        termsOfUse: termsStore.termsOfUse.map(t => t.id),
        allTermsAccepted: termsStore.allTermsAccepted,
        expectedLength: termsStore.termsOfUse.length,
        actualLength: termsStore.acceptedTerms.length
      })
    }
  } else {
    // 显示下一个条款
    currentTermIndex.value++
  }
}

// 关闭条款弹窗
const closeTermsModal = () => {
  showTermsDialog.value = false
  currentTermIndex.value = 0
}

// 处理跳转到dashboard的逻辑
const handleDashboardNavigation = () => {
  // 确保状态已初始化
  termsStore.initTermsState()
  
  // 使用nextTick确保状态更新完成后再检查
  nextTick(() => {
    if (termsStore.allTermsAccepted) {
      router.push('/dashboard/data-crawling')
    } else {
      // 显示条款确认提示
      ElMessage.warning('请先确认所有使用条款后再访问数据采集功能')
      // 触发条款弹窗显示
      showTermsModal()
    }
  })
}

// 平滑滚动到指定区域
const scrollToSection = (sectionId) => {
  const element = document.getElementById(sectionId)
  if (element) {
    element.scrollIntoView({ 
      behavior: 'smooth',
      block: 'start'
    })
  }
  // 滚动后关闭移动端菜单
  closeMobileMenu()
}

// 点击外部区域关闭移动端菜单
const handleClickOutside = (event) => {
  const navbar = document.querySelector('.navbar')
  
  if (isMobileMenuOpen.value && navbar && !navbar.contains(event.target)) {
    closeMobileMenu()
  }
}

// 页面加载完成后获取stars数量
onMounted(() => {
  fetchOriginGitHubStars()
  fetchGitHubStars()
  
  // 初始化条款状态
  termsStore.initTermsState()
  
  // 导航栏滚动效果
  window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar')
    if (window.scrollY > 50) {
      navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)'
    } else {
      navbar.style.boxShadow = 'none'
    }
    
    // 滚动时关闭移动端菜单
    closeMobileMenu()
  })
  
  // 添加点击外部区域关闭菜单的事件监听
  document.addEventListener('click', handleClickOutside)
})

// 组件卸载时清理事件监听器
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
:root {
  --primary: #2563eb;
  --primary-light: #3b82f6;
  --secondary: #64748b;
  --accent: #0ea5e9;
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --text-light: #94a3b8;
  --bg-primary: #ffffff;
  --bg-secondary: #f8fafc;
  --bg-tertiary: #f1f5f9;
  --border: #e2e8f0;
  --border-light: #f1f5f9;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.intro-page {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: linear-gradient(135deg, #ffffff 0%, #ffffff 40%, #fce7f3 80%, #fed7aa 100%);
  color: var(--text-primary);
  line-height: 1.7;
  font-size: 16px;
  min-height: 100vh;
}

/* 导航栏 */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border);
  z-index: 1000;
  padding: 1rem 0;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 3rem; /* 增加nav-brand和nav-links之间的距离 */
}

.nav-brand h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
}
/* 移动端按钮组样式 */
.mobile-nav-actions {
  display: none;
  align-items: center;
  gap: 0.5rem;
}

/* 移动端GitHub按钮样式 */
.mobile-github-btn {
  display: none;
  width: 40px;
  height: 40px;
  background: var(--primary);
  border-radius: 8px;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  transition: all 0.3s ease;
}

.mobile-github-btn:hover {
  background: var(--primary-dark);
  transform: scale(1.05);
}

.mobile-github-btn i {
  font-size: 18px;
  color: white;
}

/* 汉堡菜单按钮 */
.mobile-menu-toggle {
  display: none;
  justify-content: center;
  align-items: center;
  width: 40px;
  height: 40px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 8px;
  z-index: 1001;
  border-radius: 6px;
  transition: background-color 0.2s ease;
}

.mobile-menu-toggle:hover {
  background: rgba(0, 0, 0, 0.05);
}

.mobile-menu-toggle i {
  font-size: 20px;
  color: var(--text-primary);
  transition: all 0.3s ease;
}

.mobile-menu-toggle.active i {
  transform: rotate(90deg);
}

/* 桌面端GitHub按钮 */
.desktop-github-btn {
  display: inline-flex;
}

/* 导航栏链接样式 */
.nav-links {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.nav-links a {
  text-decoration: none;
  color: var(--text-secondary);
  font-weight: 500;
  transition: color 0.2s ease;
  cursor: pointer;
}

.nav-links a:hover {
  color: var(--primary);
}

.github-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--bg-secondary);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  border: 1px solid var(--border);
  transition: all 0.2s ease;
}

.github-link:hover {
  background: var(--primary);
  color: white !important;
  border-color: var(--primary);
}

.github-stars {
  background: rgba(255, 255, 255, 0.2);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
}

/* 英雄区域 */
.hero {
  padding: 120px 0 80px;
  background: transparent;
}

.hero-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  text-align: center;
}

.hero-badge {
  display: inline-block;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 2rem;
  border: 1px solid var(--border);
}

.hero-title {
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 700;
  line-height: 1.1;
  color: var(--text-primary);
  margin-bottom: 1.5rem;
  letter-spacing: -0.02em;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto 3rem;
  line-height: 1.6;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 1rem 2rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary {
  background: #0f172a !important;
  color: white !important;
}

.btn-primary:hover {
  background: #0f172a !important;
  color: white !important;
  transform: translateY(-2px);
}

.btn-outline {
  background: transparent;
  color: var(--text-primary);
  border: 2px solid var(--border);
}

.btn-outline:hover {
  background: var(--primary);
  color: rgb(130, 24, 216); /** 鼠标悬停时 改变在线文档打开链接按钮 文字颜色 */
  border-color: var(--primary);
  transform: translateY(-2px);
}

.btn-large {
  padding: 1.25rem 2.5rem;
  font-size: 1.1rem;
}

.btn-small {
  padding: 0.5rem 1.75rem;
  font-size: 1.2rem;
}

.star-count {
  background: rgba(255, 255, 255, 0.2);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
}

/* 功能特色 */
.features {
  padding: 80px 0;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.section-header {
  text-align: center;
  margin-bottom: 4rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
}

.section-subtitle {
  font-size: 1.1rem;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  padding: 2rem;
  transition: all 0.2s ease;
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.feature-card:hover {
  border-color: var(--primary);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  transform: translateY(-5px);
}

.feature-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  margin: 0 auto 1.5rem;
  color: white;
}

.feature-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.75rem;
}

.feature-description {
  color: var(--text-secondary);
  line-height: 1.6;
}

/* 统计数据 */
.stats {
  padding: 80px 0;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  transition: all 0.2s ease;
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.stat-card:hover {
  border-color: var(--primary);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  transform: translateY(-3px);
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--primary);
  margin-bottom: 0.5rem;
}

.stat-label {
  color: var(--text-secondary);
  font-size: 1rem;
  font-weight: 500;
}

/* 支持的平台 */
.platforms {
  padding: 80px 0;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
}

.platforms-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.platform-card {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  transition: all 0.2s ease;
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.platform-card:hover {
  border-color: var(--primary);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  transform: translateY(-4px);
}

.platform-icon {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.platform-card h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.platform-card p {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

/* 在线文档区域 */
.docs {
  padding: 80px 0;
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(10px);
}

.docs-content {
  margin-top: 3rem;
}

.docs-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 3rem;
  align-items: start;
}

.docs-preview {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.docs-preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border);
}

.docs-preview-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

.docs-iframe-container {
  position: relative;
  width: 100%;
  height: 500px;
  overflow: hidden;
}

.docs-iframe {
  width: 100%;
  height: 100%;
  border: none;
  background: white;
}

.docs-links {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.docs-links h3 {
  margin: 0 0 1.5rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

.docs-link-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.docs-link-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: 8px;
  text-decoration: none;
  color: var(--text-primary);
  transition: all 0.2s ease;
}

.docs-link-item:hover {
  background: var(--primary);
  color: rgb(99, 92, 92); /** 鼠标悬停时 改变在线文档指示标题 颜色 */
  border-color: var(--primary);
  transform: translateX(5px);
}

.docs-link-icon {
  width: 40px;
  height: 40px;
  background: var(--bg-tertiary);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  color: var(--primary);
  transition: all 0.2s ease;
}

.docs-link-item:hover .docs-link-icon {
  background: rgba(255, 255, 255, 0.2);
  color: rgb(100, 5, 104); /** 鼠标悬停时 改变在线文档图标 颜色 */
}

.docs-link-content {
  flex: 1;
}

.docs-link-content h4 {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
  font-weight: 600;
}

.docs-link-content p {
  margin: 0;
  font-size: 0.875rem;
  color: var(--text-secondary);
  transition: color 0.2s ease;
}

.docs-link-item:hover .docs-link-content p {
  color: rgba(236, 21, 201, 0.8); /** 鼠标悬停时 改变在线文档指示文本 颜色 */
}

/* CTA区域 */
.cta {
  padding: 80px 0;
  text-align: center;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
}

.cta-content {
  max-width: 600px;
  margin: 0 auto;
}

.cta-title {
  font-size: 2.25rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
}

.cta-subtitle {
  font-size: 1.1rem;
  color: var(--text-secondary);
  margin-bottom: 2rem;
  line-height: 1.6;
}



/* 响应式设计 */
@media (max-width: 1024px) {
  .nav-container {
    gap: 2rem;
  }
  
  .nav-links {
    gap: 1.2rem;
  }
  
  /* 平板设备GitHub按钮优化 */
  .nav-links .btn.btn-primary {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }
  
  .nav-links .github-stars {
    font-size: 0.8rem;
  }
  
  .docs-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .docs-iframe-container {
    height: 400px;
  }
}

@media (max-width: 768px) {
  .navbar {
    padding: 0.75rem 0;
  }
  
  .nav-container {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    padding: 0 1rem;
  }
  
  .nav-brand h2 {
    font-size: 1.25rem;
  }
  
  /* 显示移动端按钮组 */
  .mobile-nav-actions {
    display: flex;
  }
  
  /* 显示移动端GitHub按钮 */
  .mobile-github-btn {
    display: flex;
  }
  
  /* 显示汉堡菜单按钮 */
  .mobile-menu-toggle {
    display: flex;
  }
  
  /* 隐藏桌面端GitHub按钮 */
  .desktop-github-btn {
    display: none;
  }
  
  /* 在移动端隐藏导航链接 */
  .nav-links {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: rgba(255, 255, 255, 0.98);
    backdrop-filter: blur(10px);
    border-top: 1px solid var(--border);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    flex-direction: column;
    gap: 0;
    padding: 1rem 0;
    z-index: 1000;
  }
  
  .nav-links.mobile-open {
    display: flex;
  }
  
  .nav-links a {
    padding: 1rem 2rem;
    border-radius: 0;
    background: transparent;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    width: 100%;
    text-align: left;
    font-size: 1rem;
  }
  
  .nav-links a:hover {
    background: rgba(37, 99, 235, 0.05);
  }
  
  /* 移动端GitHub按钮样式 */
  .nav-links .github-link {
    margin: 0.5rem 2rem;
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
    border-radius: 8px;
    width: auto;
    text-align: center;
  }
  
  .nav-links .github-stars {
    font-size: 0.8rem;
  }
  
  .hero {
    padding: 100px 0 60px;
  }
  
  .hero-container {
    padding: 0 1rem;
  }
  
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .features, .platforms, .cta, .docs {
    padding: 60px 0;
  }
  
  .container {
    padding: 0 1rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .hero-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .btn {
    width: 100%;
    max-width: 300px;
    justify-content: center;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
  
  .platforms-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
  
  .docs-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .docs-preview-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
    padding: 1rem;
  }
  
  .docs-iframe-container {
    height: 300px;
  }
  
  .docs-links {
    padding: 1.5rem;
  }
  
  .docs-link-item {
    padding: 0.75rem;
    gap: 0.75rem;
  }
  
  .docs-link-icon {
    width: 35px;
    height: 35px;
    font-size: 1rem;
  }
  
  .docs-link-content h4 {
    font-size: 0.9rem;
  }
  
  .docs-link-content p {
    font-size: 0.8rem;
  }
  
  .modal-content {
    margin: 1rem;
    max-height: 90vh;
  }
  
  .modal-header,
  .modal-body,
  .modal-footer {
    padding: 1rem 1.5rem;
  }
  
  .modal-footer {
    flex-direction: column;
  }
  
  .modal-footer .btn {
    width: 100%;
    min-width: auto;
  }
}

@media (max-width: 480px) {
  .nav-links a {
    font-size: 0.9rem;
    padding: 0.875rem 1.5rem;
  }
  
  .nav-links .github-link {
    margin: 0.5rem 1.5rem;
    padding: 0.625rem 0.875rem;
    font-size: 0.8rem;
  }
  
  .nav-links .github-stars {
    font-size: 0.7rem;
  }
  
  .hero-title {
    font-size: 1.75rem;
  }
  
  .hero-subtitle {
    font-size: 1rem;
  }
  
  .section-title {
    font-size: 1.75rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .platforms-grid {
    grid-template-columns: 1fr;
  }
  
  .docs-iframe-container {
    height: 250px;
  }
  
  .docs-link-item {
    flex-direction: column;
    text-align: center;
    gap: 0.5rem;
  }
  
  .docs-link-item:hover {
    transform: none;
  }
}

/* 条款弹窗样式 */
.terms-modal-content {
  padding: 1rem 0;
}

.terms-progress {
  margin-bottom: 2rem;
}

.progress-text {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
  text-align: center;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: var(--bg-tertiary);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary), var(--primary-light));
  border-radius: 4px;
  transition: width 0.3s ease;
}

.current-term {
  margin-bottom: 1.5rem;
}

.term-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--border);
}

.term-content {
  font-size: 1rem;
  line-height: 1.6;
  color: var(--text-secondary);
  background: var(--bg-secondary);
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid var(--primary);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

/* 弹窗深度样式修复 */
:deep(.el-dialog) {
  border-radius: 12px;
  overflow: hidden;
}

:deep(.el-dialog__header) {
  background: var(--bg-secondary);
  padding: 1.5rem 2rem 1rem;
  border-bottom: 1px solid var(--border);
}

:deep(.el-dialog__title) {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

:deep(.el-dialog__body) {
  padding: 2rem;
}

:deep(.el-dialog__footer) {
  padding: 1rem 2rem 1.5rem;
  background: var(--bg-secondary);
  border-top: 1px solid var(--border);
}

:deep(.el-alert) {
  border-radius: 8px;
}
</style>