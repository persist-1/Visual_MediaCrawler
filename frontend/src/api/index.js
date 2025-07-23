import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 在发送请求之前做些什么
    console.log('Request:', config.method?.toUpperCase(), config.url)
    return config
  },
  (error) => {
    // 对请求错误做些什么
    console.error('Request Error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    // 对响应数据做点什么
    console.log('Response:', response.status, response.config.url)
    return response.data
  },
  (error) => {
    // 对响应错误做点什么
    console.error('Response Error:', error.response?.status, error.response?.data || error.message)
    
    // 统一错误处理
    const message = error.response?.data?.detail || error.response?.data?.message || error.message || '请求失败'
    
    return Promise.reject({
      status: error.response?.status,
      message,
      data: error.response?.data
    })
  }
)

// 爬虫API
export const crawlerAPI = {
  // 同步执行爬虫任务
  runSync: (data) => api.post('/crawler/run', data),
  
  // 异步执行爬虫任务
  runAsync: (data) => api.post('/crawler/run-async', data),
  
  // 获取任务状态
  getTaskStatus: (taskId) => api.get(`/crawler/task/${taskId}`),
  
  // 获取所有任务
  getAllTasks: (database = 'sqlite') => api.get(`/crawler/tasks?database=${database}`),
  
  // 删除任务
  deleteTask: (taskId) => api.delete(`/crawler/task/${taskId}`)
}

// 系统API
export const systemAPI = {
  // 健康检查
  getHealth: () => api.get('/health'),
  
  // 获取根信息
  getRoot: () => api.get('/')
}

// 平台选项
export const PLATFORMS = [
  { value: 'xhs', label: '小红书', icon: 'iconfont icon-xiaohongshu-hui' },
  { value: 'dy', label: '抖音', icon: 'iconfont icon-douyin' },
  { value: 'ks', label: '快手', icon: 'iconfont icon-kuaishou' },
  { value: 'bili', label: '哔哩哔哩', icon: 'iconfont icon-bilibili' },
  { value: 'wb', label: '微博', icon: 'iconfont icon-weibo' },
  { value: 'tieba', label: '贴吧', icon: 'iconfont icon-social-tieba' },
  { value: 'zhihu', label: '知乎', icon: 'iconfont icon-zhihu' }
]

// 平台格式样例
export const PLATFORM_EXAMPLES = {
  xhs: {
    detail: {
      title: '详情页URL格式',
      examples: [
        'https://www.xiaohongshu.com/explore/66fad51c000000001b0224b8?xsec_token=AB3rO-QopW5sgrJ41GwN01WCXh6yWPxjSoFI9D5JIMgKw=&xsec_source=pc_search'
      ],
      description: '需要携带xsec_token和xsec_source参数'
    },
    creator: {
      title: '创作者ID格式',
      examples: [
        '63e36c9a000000002703502b'
      ],
      description: '纯数字+字母组合的ID'
    }
  },
  dy: {
    detail: {
      title: '详情页ID格式',
      examples: [
        '7280854932641664319',
        '7202432992642387233'
      ],
      description: '纯数字ID'
    },
    creator: {
      title: '创作者ID格式',
      examples: [
        'MS4wLjABAAAATJPY7LAlaa5X-c8uNdWkvz0jUGgpw4eeXIwu_8BhvqE'
      ],
      description: 'sec_id格式，包含特殊字符'
    }
  },
  ks: {
    detail: {
      title: '详情页ID格式',
      examples: [
        '3xf8enb8dbj6uig',
        '3x6zz972bchmvqe'
      ],
      description: '字母+数字组合的短ID'
    },
    creator: {
      title: '创作者ID格式',
      examples: [
        '3x4sm73aye7jq7i'
      ],
      description: '与详情页ID格式相似'
    }
  },
  bili: {
    detail: {
      title: '详情页ID格式',
      examples: [
        'BV1d54y1g7db',
        'BV1Sz4y1U77N',
        'BV14Q4y1n7jz'
      ],
      description: 'BV号格式'
    },
    creator: {
      title: '创作者ID格式',
      examples: [
        '20813884'
      ],
      description: '纯数字UID'
    }
  },
  wb: {
    detail: {
      title: '详情页ID格式',
      examples: [
        '4982041758140155'
      ],
      description: '长数字ID'
    },
    creator: {
      title: '创作者ID格式',
      examples: [
        '5533390220'
      ],
      description: '数字UID'
    }
  },
  tieba: {
    detail: {
      title: '详情页ID格式',
      examples: [],
      description: '格式待定'
    },
    creator: {
      title: '创作者URL格式',
      examples: [
        'https://tieba.baidu.com/home/main/?id=tb.1.7f139e2e.6CyEwxu3VJruH_-QqpCi6g&fr=frs'
      ],
      description: '完整的用户主页URL'
    }
  },
  zhihu: {
    detail: {
      title: '详情页URL格式',
      examples: [
        'https://www.zhihu.com/question/826896610/answer/4885821440',
        'https://zhuanlan.zhihu.com/p/673461588',
        'https://www.zhihu.com/zvideo/1539542068422144000'
      ],
      description: '支持多种内容类型的完整URL（回答/文章/视频）'
    },
    creator: {
      title: '创作者URL格式',
      examples: [
        'https://www.zhihu.com/people/yd1234567'
      ],
      description: '用户主页完整URL'
    }
  }
}

// 登录类型
export const LOGIN_TYPES = [
  { value: 'qrcode', label: '二维码登录' },
  { value: 'phone', label: '手机号登录' },
  { value: 'cookie', label: 'Cookie登录' }
]

// 爬虫类型
export const CRAWLER_TYPES = [
  { value: 'search', label: '关键词搜索' },
  { value: 'detail', label: '详情页爬取' },
  { value: 'creator', label: '创作者主页' }
]

// 保存选项
export const SAVE_OPTIONS = [
  { value: 'csv', label: 'CSV文件' },
  { value: 'json', label: 'JSON文件' },
  { value: 'db', label: '数据库' }
]

// WebSocket管理器
export class WebSocketManager {
  constructor(url) {
    this.url = url
    this.ws = null
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
    this.reconnectInterval = 3000
    this.listeners = new Map()
  }

  connect() {
    try {
      this.ws = new WebSocket(this.url)
      
      this.ws.onopen = () => {
        console.log('WebSocket connected:', this.url)
        this.reconnectAttempts = 0
        this.emit('connected')
      }
      
      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          this.emit('message', data)
        } catch (error) {
          console.error('WebSocket message parse error:', error)
        }
      }
      
      this.ws.onclose = () => {
        console.log('WebSocket disconnected:', this.url)
        this.emit('disconnected')
        this.reconnect()
      }
      
      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error)
        this.emit('error', error)
      }
    } catch (error) {
      console.error('WebSocket connection failed:', error)
      this.reconnect()
    }
  }

  reconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      console.log(`WebSocket reconnecting... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`)
      
      setTimeout(() => {
        this.connect()
      }, this.reconnectInterval)
    } else {
      console.error('WebSocket max reconnect attempts reached')
      this.emit('maxReconnectReached')
    }
  }

  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data))
    } else {
      console.warn('WebSocket is not connected')
    }
  }

  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, [])
    }
    this.listeners.get(event).push(callback)
  }

  off(event, callback) {
    if (this.listeners.has(event)) {
      const callbacks = this.listeners.get(event)
      const index = callbacks.indexOf(callback)
      if (index > -1) {
        callbacks.splice(index, 1)
      }
    }
  }

  emit(event, data) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).forEach(callback => {
        try {
          callback(data)
        } catch (error) {
          console.error('WebSocket event callback error:', error)
        }
      })
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
    this.listeners.clear()
  }
}

// 创建日志WebSocket实例
export const createLogWebSocket = (taskId) => {
  // TODO: 实现日志WebSocket连接
  console.log('Log WebSocket not implemented yet for task:', taskId)
  return null
}

// 创建进度WebSocket实例
export const createProgressWebSocket = (taskId) => {
  // TODO: 实现进度WebSocket连接
  console.log('Progress WebSocket not implemented yet for task:', taskId)
  return null
}

export default api