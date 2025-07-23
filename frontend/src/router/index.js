import { createRouter, createWebHistory } from 'vue-router'
import DataCrawler from '../views/DataCrawler.vue'
import DataShow from '../views/DataShow.vue'
import Intro from '../views/Intro.vue'
import { useTermsStore } from '@/stores/terms'
import { ElMessage } from 'element-plus'

const routes = [
  {
    path: '/',
    redirect: '/intro'
  },
  {
    path: '/intro',
    name: 'Intro',
    component: Intro,
    meta: {
      title: '项目介绍'
    }
  },
  {
    path: '/dashboard/data-crawling',
    name: 'DataCrawling',
    component: DataCrawler,
    meta: {
      title: '数据爬取'
    }
  },
  {
    path: '/dashboard/data-show',
    name: 'DataShow',
    component: DataShow,
    meta: {
      title: '数据展示'
    }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 路由守卫：保护dashboard页面
router.beforeEach((to, from, next) => {
  // 检查是否访问dashboard相关页面
  if (to.path.startsWith('/dashboard')) {
    const termsStore = useTermsStore()
    
    // 初始化条款状态
    termsStore.initTermsState()
    
    // 检查是否所有条款都已确认
    if (!termsStore.allTermsAccepted) {
      ElMessage.warning('请先确认所有使用条款后再访问数据采集功能')
      next('/intro')
      return
    }
  }
  
  next()
})

export default router