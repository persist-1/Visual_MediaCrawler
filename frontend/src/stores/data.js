import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

// 数据表配置
const TABLE_CONFIG = {
  bilibili_video: {
    label: 'B站视频',
    icon: 'fab fa-bilibili',
    columns: [
      { prop: 'video_id', label: '视频ID', width: '120' },
      { prop: 'video_url', label: '视频链接', minWidth: '200' },
      { prop: 'title', label: '标题', minWidth: '300' },
      { prop: 'desc', label: '描述', minWidth: '200' },
      { prop: 'create_time', label: '发布时间', width: '180', formatter: (row) => formatDateTime(row.create_time) },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'nickname', label: '昵称', width: '150' },
      { prop: 'video_play_count', label: '播放量', width: '100' },
      { prop: 'video_danmaku', label: '弹幕数', width: '100' },
      { prop: 'video_comment', label: '评论数', width: '100' },
      { prop: 'liked_count', label: '点赞数', width: '100' },
      { prop: 'video_share_count', label: '分享数', width: '100' },
      { prop: 'video_favorite_count', label: '收藏数', width: '120' },
      { prop: 'video_coin_count', label: '投币数', width: '100' }
    ]
  },
  douyin_aweme: {
    label: '抖音视频',
    icon: 'fas fa-music',
    columns: [
      { prop: 'aweme_id', label: '视频ID', width: '120' },
      { prop: 'aweme_url', label: '视频链接', minWidth: '200' },
      { prop: 'desc', label: '描述', minWidth: '300' },
      { prop: 'create_time', label: '发布时间', width: '180', formatter: (row) => formatDateTime(row.create_time) },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'nickname', label: '昵称', width: '150' },
      { prop: 'liked_count', label: '点赞数', width: '100' },
      { prop: 'comment_count', label: '评论数', width: '100' },
      { prop: 'share_count', label: '分享数', width: '100' },
      { prop: 'collected_count', label: '收藏数', width: '100' }
    ]
  },
  kuaishou_video: {
    label: '快手视频',
    icon: 'fas fa-video',
    columns: [
      { prop: 'video_id', label: '视频ID', width: '120' },
      { prop: 'video_url', label: '视频链接', minWidth: '200' },
      { prop: 'title', label: '标题', minWidth: '300' },
      { prop: 'desc', label: '描述', minWidth: '200' },
      { prop: 'create_time', label: '发布时间', width: '180', formatter: (row) => formatDateTime(row.create_time) },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'nickname', label: '昵称', width: '150' },
      { prop: 'viewd_count', label: '播放量', width: '100' },
      { prop: 'liked_count', label: '点赞数', width: '100' }
    ]
  },
  xhs_note: {
    label: '小红书笔记',
    icon: 'fas fa-book',
    columns: [
      { prop: 'note_id', label: '笔记ID', width: '120' },
      { prop: 'note_url', label: '笔记链接', minWidth: '200' },
      { prop: 'title', label: '标题', minWidth: '300' },
      { prop: 'desc', label: '描述', minWidth: '200' },
      { prop: 'time', label: '发布时间', width: '180', formatter: (row) => formatDateTime(row.time) },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'nickname', label: '昵称', width: '150' },
      { prop: 'liked_count', label: '点赞数', width: '100' },
      { prop: 'collected_count', label: '收藏数', width: '100' },
      { prop: 'comment_count', label: '评论数', width: '100' },
      { prop: 'share_count', label: '分享数', width: '100' }
    ]
  },
  weibo_note: {
    label: '微博内容',
    icon: 'fab fa-weibo',
    columns: [
      { prop: 'note_id', label: '微博ID', width: '120' },
      { prop: 'note_url', label: '微博链接', minWidth: '200' },
      { prop: 'content', label: '内容', minWidth: '300' },
      { prop: 'create_time', label: '发布时间', width: '180', formatter: (row) => formatDateTime(row.create_time) },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'nickname', label: '昵称', width: '150' },
      { prop: 'liked_count', label: '点赞数', width: '100' },
      { prop: 'comments_count', label: '评论数', width: '100' },
      { prop: 'shared_count', label: '转发数', width: '100' }
    ]
  },
  tieba_note: {
    label: '贴吧帖子',
    icon: 'fas fa-comments',
    columns: [
      { prop: 'note_id', label: '帖子ID', width: '120' },
      { prop: 'note_url', label: '帖子链接', minWidth: '200' },
      { prop: 'title', label: '标题', minWidth: '300' },
      { prop: 'desc', label: '内容', minWidth: '300' },
      { prop: 'publish_time', label: '发布时间', width: '180' },
      { prop: 'user_nickname', label: '昵称', width: '150' },
      { prop: 'tieba_name', label: '贴吧名', width: '120' },
      { prop: 'total_replay_num', label: '回复数', width: '100' }
    ]
  },
  zhihu_content: {
    label: '知乎内容',
    icon: 'fab fa-zhihu',
    columns: [
      { prop: 'content_id', label: '内容ID', width: '120' },
      { prop: 'content_url', label: '内容链接', minWidth: '200' },
      { prop: 'title', label: '标题', minWidth: '300' },
      { prop: 'desc', label: '内容', minWidth: '300' },
      { prop: 'created_time', label: '发布时间', width: '180' },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'user_nickname', label: '昵称', width: '150' },
      { prop: 'voteup_count', label: '赞同数', width: '100' },
      { prop: 'comment_count', label: '评论数', width: '100' }
    ]
  }
}

// 时间格式化函数
const formatDateTime = (timestamp) => {
  if (!timestamp) return '--'
  const date = new Date(timestamp * 1000)
  return date.toLocaleString('zh-CN')
}

export const useDataStore = defineStore('data', () => {
  // 状态
  const loading = ref(false)
  const tableData = ref([])
  const totalCount = ref(0)
  const availableTables = ref([])
  const tableColumns = ref([])

  // 计算属性
  const hasData = computed(() => tableData.value.length > 0)

  // 方法
  const loadAvailableTables = async () => {
    try {
      const response = await axios.get('/api/sqlite/tables')
      const tables = response.data.data || []
      
      availableTables.value = tables.map(tableName => {
        const config = TABLE_CONFIG[tableName]
        return {
          value: tableName,
          label: config ? config.label : tableName,
          icon: config ? config.icon : 'fas fa-table'
        }
      })
    } catch (error) {
      console.error('加载数据表列表失败:', error)
      throw new Error('加载数据表列表失败')
    }
  }

  const loadTableData = async ({ table, page = 1, pageSize = 30, taskId = undefined }) => {
    loading.value = true
    try {
      const params = { table, page, page_size: pageSize }
      if (taskId) {
        params.task_times_id = taskId
      }
      
      const response = await axios.get('/api/sqlite/data', {
        params
      })
      
      const result = response.data.data
      tableData.value = result.data || []
      totalCount.value = result.total || 0
      
      // 设置表格列配置
      const config = TABLE_CONFIG[table]
      if (config) {
        tableColumns.value = config.columns
      } else {
        // 如果没有预定义配置，动态生成列
        if (tableData.value.length > 0) {
          const firstRow = tableData.value[0]
          tableColumns.value = Object.keys(firstRow).map(key => ({
            prop: key,
            label: key,
            minWidth: '150'
          }))
        }
      }
    } catch (error) {
      console.error('加载表格数据失败:', error)
      throw new Error('加载表格数据失败')
    } finally {
      loading.value = false
    }
  }



  const exportTableData = async (tableName, taskId = null) => {
    try {
      const params = new URLSearchParams()
      params.append('table_name', tableName)
      if (taskId) {
        params.append('task_id', taskId)
      }
      
      const response = await axios.get('/api/sqlite/export', {
        params: Object.fromEntries(params),
        responseType: 'blob'
      })
      
      // 创建下载链接
      const blob = new Blob([response.data], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `${tableName}_${new Date().toISOString().split('T')[0]}.csv`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('导出CSV数据失败:', error)
      throw error
    }
  }

  const exportTableDataAsJSON = async (tableName, taskId = null) => {
    try {
      const params = new URLSearchParams()
      params.append('table_name', tableName)
      if (taskId) {
        params.append('task_id', taskId)
      }
      
      const response = await axios.get('/api/sqlite/export-json', {
        params: Object.fromEntries(params)
      })
      
      // 创建JSON文件下载
      const jsonData = JSON.stringify(response.data, null, 2)
      const blob = new Blob([jsonData], { type: 'application/json' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `${tableName}_${new Date().toISOString().split('T')[0]}.json`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('导出JSON数据失败:', error)
      throw error
    }
  }

  return {
    // 状态
    loading,
    tableData,
    totalCount,
    availableTables,
    tableColumns,
    
    // 计算属性
    hasData,
    
    // 方法
    loadAvailableTables,
    loadTableData,
    exportTableData,
    exportTableDataAsJSON
  }
})