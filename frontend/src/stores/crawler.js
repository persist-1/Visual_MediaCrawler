import { defineStore } from 'pinia'
import { crawlerAPI, systemAPI } from '../api'

export const useCrawlerStore = defineStore('crawler', {
  state: () => ({
    // 任务列表
    tasks: [],
    // 当前任务
    currentTask: null,
    // 系统状态
    systemStatus: {
      status: 'unknown',
      message: '未知状态'
    },
    // 加载状态
    loading: {
      tasks: false,
      submit: false,
      status: false
    },
    // 表单数据
    formData: {
        platform: 'bili',
        lt: 'cookie',
        type: 'search',
        start: 1,
        max_count: 50,
        keywords: '',
        detail_urls: '',
        creator_ids: '',
        get_comment: false,
        get_sub_comment: false,
        sync_to_mysql: false,
        cookies: ''
      }
  }),

  getters: {
    // 运行中的任务
    runningTasks: (state) => {
      return state.tasks.filter(task => task.status === 'running')
    },
    // 已完成的任务
    completedTasks: (state) => {
      return state.tasks.filter(task => task.status === 'completed')
    },
    // 失败的任务
    failedTasks: (state) => {
      return state.tasks.filter(task => task.status === 'failed')
    },
    // 任务统计
    taskStats: (state) => {
      const total = state.tasks.length
      const running = state.tasks.filter(t => t.status === 'running').length
      const completed = state.tasks.filter(t => t.status === 'completed').length
      const failed = state.tasks.filter(t => t.status === 'failed').length
      
      return { total, running, completed, failed }
    }
  },

  actions: {
    // 提交同步任务
    async submitSyncTask(formData) {
      this.loading.submit = true
      try {
        const response = await crawlerAPI.runSync(formData)
        if (response.success) {
          // 同步任务直接返回结果
          return {
            success: true,
            data: response.data,
            message: response.message
          }
        } else {
          throw new Error(response.message)
        }
      } catch (error) {
        console.error('提交同步任务失败:', error)
        throw error
      } finally {
        this.loading.submit = false
      }
    },

    // 提交异步任务
    async submitAsyncTask(formData) {
      this.loading.submit = true
      try {
        const response = await crawlerAPI.runAsync(formData)
        if (response.success) {
          // 添加到任务列表
          const newTask = {
            task_times_id: response.task_times_id,
            status: 'running',
            message: response.message,
            created_at: new Date().toISOString(),
            formData: { ...formData }
          }
          this.tasks.unshift(newTask)
          return newTask
        } else {
          throw new Error(response.message)
        }
      } catch (error) {
        console.error('提交异步任务失败:', error)
        throw error
      } finally {
        this.loading.submit = false
      }
    },

    // 获取任务状态
    async getTaskStatus(taskId) {
      if (!taskId || taskId === 'undefined') {
        throw new Error('无效的任务ID')
      }
      try {
        const response = await crawlerAPI.getTaskStatus(taskId)
        // 更新任务列表中的任务状态
        const taskIndex = this.tasks.findIndex(t => t.task_times_id === taskId)
        if (taskIndex !== -1) {
          this.tasks[taskIndex] = {
            ...this.tasks[taskIndex],
            ...response,
            // 确保有updated_at字段
            updated_at: response.updated_at || new Date().toISOString()
          }
        }
        return response
      } catch (error) {
        console.error('获取任务状态失败:', error)
        throw error
      }
    },

    // 获取所有任务
    async getAllTasks() {
      this.loading.tasks = true
      try {
        const response = await crawlerAPI.getAllTasks()
        // 直接使用服务器返回的任务数据
        const serverTasks = response.tasks || []
        
        // 保留服务器返回的完整任务信息
        this.tasks = serverTasks.map(serverTask => ({
          ...serverTask,
          // 确保有created_at字段
          created_at: serverTask.created_at || new Date().toISOString(),
          // 确保有updated_at字段
          updated_at: serverTask.updated_at || new Date().toISOString()
        }))
      } catch (error) {
        console.error('获取任务列表失败:', error)
      } finally {
        this.loading.tasks = false
      }
    },

    // 删除任务
    async deleteTask(taskId) {
      if (!taskId || taskId === 'undefined') {
        throw new Error('无效的任务ID')
      }
      try {
        await crawlerAPI.deleteTask(taskId)
        // 从本地任务列表中移除
        const taskIndex = this.tasks.findIndex(t => t.task_times_id === taskId)
        if (taskIndex !== -1) {
          this.tasks.splice(taskIndex, 1)
        }
      } catch (error) {
        console.error('删除任务失败:', error)
        throw error
      }
    },

    // 获取系统状态
    async getSystemStatus() {
      this.loading.status = true
      try {
        const response = await systemAPI.healthCheck()
        this.systemStatus = {
          status: response.status,
          message: response.message
        }
      } catch (error) {
        console.error('获取系统状态失败:', error)
        this.systemStatus = {
          status: 'error',
          message: '系统连接失败'
        }
      } finally {
        this.loading.status = false
      }
    },

    // 重置表单
    resetForm() {
      this.formData = {
        platform: 'bili',
        lt: 'cookie',
        type: 'search',
        start: 1,
        max_count: 50,
        keywords: '',
        detail_urls: '',
        creator_ids: '',
        get_comment: false,
        get_sub_comment: false,
        sync_to_mysql: false,
        cookies: ''
      }
    },

    // 设置当前任务
    setCurrentTask(task) {
      this.currentTask = task
    },

    // 批量更新任务状态
    async refreshRunningTasks() {
      const runningTasks = this.tasks.filter(t => t.status === 'running' && t.task_times_id)
      const promises = runningTasks
        .filter(task => task.task_times_id && task.task_times_id !== 'undefined')
        .map(task => this.getTaskStatus(task.task_times_id))
      
      try {
        await Promise.allSettled(promises)
      } catch (error) {
        console.error('批量更新任务状态失败:', error)
      }
    }
  }
})