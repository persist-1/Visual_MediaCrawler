/**
 * 全局 z-index 配置
 * 用于统一管理项目中所有弹窗和浮层的层级关系
 */

// 基础层级
export const Z_INDEX_BASE = 1000

// 弹窗层级
export const Z_INDEX_DIALOG = {
  // 条款状态弹窗
  TERMS_DIALOG_OVERLAY: 5001,
  TERMS_DIALOG_WRAPPER: 5002,
  TERMS_DIALOG: 5003,
  
  // 确认取消弹窗（需要比条款弹窗更高）
  CONFIRM_DIALOG_OVERLAY: 5010,
  CONFIRM_DIALOG_WRAPPER: 5011,
  CONFIRM_DIALOG: 5011 ,
}

// 消息提示层级
export const Z_INDEX_MESSAGE = {
  MESSAGE: 3000,
  NOTIFICATION: 4000
}

// 加载层级
export const Z_INDEX_LOADING = {
  LOADING: 2000
}

// 工具提示层级
export const Z_INDEX_TOOLTIP = {
  TOOLTIP: 2500
}

// 导出所有z-index配置
export default {
  BASE: Z_INDEX_BASE,
  DIALOG: Z_INDEX_DIALOG,
  MESSAGE: Z_INDEX_MESSAGE,
  LOADING: Z_INDEX_LOADING,
  TOOLTIP: Z_INDEX_TOOLTIP
}