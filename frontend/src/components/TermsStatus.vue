<template>
  <div class="terms-status">
    <el-button 
      type="text" 
      size="small" 
      @click="showTermsDialog = true"
      :class="{ 'terms-accepted': allTermsAccepted, 'terms-pending': !allTermsAccepted }"
    >
      <el-icon><DocumentChecked /></el-icon>
      条款状态 ({{ acceptedTerms.length }}/{{ termsOfUse.length }})
    </el-button>

    <!-- 条款状态弹窗 -->
    <el-dialog 
      v-model="showTermsDialog" 
      title="使用条款确认状态" 
      width="70%"
      :before-close="handleClose"
      append-to-body
      :z-index="Z_INDEX_DIALOG.TERMS_DIALOG"
    >
      <div class="terms-dialog-content">
        <div class="terms-summary">
          <el-alert
            :title="allTermsAccepted ? '所有条款已确认' : `还有 ${unacceptedTerms.length} 项条款待确认`"
            :type="allTermsAccepted ? 'success' : 'warning'"
            :closable="false"
            show-icon
          />
        </div>

        <div class="terms-list">
          <div 
            v-for="term in termsOfUse" 
            :key="term.id"
            class="term-item"
            :class="{ 'accepted': isTermAccepted(term.id) }"
          >
            <div class="term-header">
              <div class="term-title">
                <el-icon v-if="isTermAccepted(term.id)" class="check-icon"><Check /></el-icon>
                <el-icon v-else class="pending-icon"><Clock /></el-icon>
                <span>{{ term.title }}</span>
              </div>
              <el-button
                v-if="isTermAccepted(term.id)"
                type="danger"
                size="small"
                @click="handleRejectTerm(term.id)"
              >
                取消确认
              </el-button>
            </div>
            <div class="term-content">
              {{ term.content }}
            </div>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showTermsDialog = false">关闭</el-button>
          <el-button 
            v-if="!allTermsAccepted" 
            type="primary" 
            @click="handleAcceptAll"
          >
            确认所有条款
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useTermsStore } from '@/stores/terms'
import { ElMessage, ElMessageBox } from 'element-plus'
import { DocumentChecked, Check, Clock } from '@element-plus/icons-vue'
import { Z_INDEX_DIALOG } from '@/config/zIndex'

const router = useRouter()
const termsStore = useTermsStore()
const showTermsDialog = ref(false)

// 计算属性
const allTermsAccepted = computed(() => termsStore.allTermsAccepted)
const acceptedTerms = computed(() => termsStore.acceptedTerms)
const unacceptedTerms = computed(() => termsStore.unacceptedTerms)
const termsOfUse = computed(() => termsStore.termsOfUse)

// 方法
const isTermAccepted = (termId) => {
  return termsStore.isTermAccepted(termId)
}

const handleRejectTerm = async (termId) => {
  try {
    // 显示确认弹窗
    const messageBoxPromise = ElMessageBox.confirm(
      '取消确认此条款将禁止您访问数据采集功能，确定要继续吗？',
      '确认取消',
      {
        confirmButtonText: '确定取消',
        cancelButtonText: '保持确认',
        type: 'warning',
        appendToBody: true,
        zIndex: Z_INDEX_DIALOG.CONFIRM_DIALOG,
      }
    )
    
    // 确保确认弹窗的z-index正确设置
    setTimeout(() => {
      const messageBoxOverlays = document.querySelectorAll('.el-overlay.is-message-box')
      const messageBoxes = document.querySelectorAll('.el-message-box')
      
      messageBoxOverlays.forEach(overlay => {
        if (overlay.style.display !== 'none') {
          overlay.style.setProperty('z-index', Z_INDEX_DIALOG.CONFIRM_DIALOG_OVERLAY, 'important')
        }
      })
      
      messageBoxes.forEach(box => {
        box.style.setProperty('z-index', Z_INDEX_DIALOG.CONFIRM_DIALOG, 'important')
      })
    }, 10)
    
    await messageBoxPromise
    
    termsStore.rejectTerm(termId)
    ElMessage.success('已取消确认该条款')
    
    // 如果当前在dashboard页面，跳转回intro页面
    if (router.currentRoute.value.path.startsWith('/dashboard')) {
      ElMessage.warning('由于条款状态变更，将返回介绍页面')
      router.push('/intro')
      showTermsDialog.value = false
    }
  } catch {
    // 用户取消操作
  }
}

const handleAcceptAll = () => {
  termsStore.acceptAllTerms()
  ElMessage.success('已确认所有使用条款')
  showTermsDialog.value = false
}

const handleClose = (done) => {
  done()
}
</script>

<style scoped>
.terms-status {
  display: flex;
  align-items: center;
}

.terms-accepted {
  color: #67c23a;
}

.terms-pending {
  color: #e6a23c;
}

/* 确保弹窗有足够高的z-index并正确显示 */
:deep(.el-overlay) {
  z-index: v-bind('Z_INDEX_DIALOG.TERMS_DIALOG_OVERLAY') !important;
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  background-color: rgba(0, 0, 0, 0.5) !important;
}

:deep(.el-dialog) {
  z-index: v-bind('Z_INDEX_DIALOG.TERMS_DIALOG') !important;
  position: relative !important;
  margin: 0 !important;
}

:deep(.el-dialog__wrapper) {
  z-index: v-bind('Z_INDEX_DIALOG.TERMS_DIALOG_WRAPPER') !important;
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  pointer-events: auto !important;
}

.terms-dialog-content {
  max-height: 60vh;
  overflow-y: auto;
}

.terms-summary {
  margin-bottom: 20px;
}

.terms-list {
  space-y: 16px;
}

.term-item {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  transition: all 0.3s ease;
}

.term-item.accepted {
  border-color: #67c23a;
  background-color: #f0f9ff;
}

.term-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.term-title {
  display: flex;
  align-items: center;
  font-weight: 600;
  font-size: 16px;
}

.check-icon {
  color: #67c23a;
  margin-right: 8px;
}

.pending-icon {
  color: #e6a23c;
  margin-right: 8px;
}

.term-content {
  color: #606266;
  line-height: 1.6;
  font-size: 14px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* 确保ElMessageBox有足够高的z-index - 使用全局样式 */
:global(.el-message-box) {
  z-index: v-bind('Z_INDEX_DIALOG.CONFIRM_DIALOG') !important;
}

:global(.el-message-box__wrapper) {
  z-index: v-bind('Z_INDEX_DIALOG.CONFIRM_DIALOG_WRAPPER') !important;
}

:global(.el-overlay.is-message-box) {
  z-index: v-bind('Z_INDEX_DIALOG.CONFIRM_DIALOG_OVERLAY') !important;
}

/* 深度选择器备用方案 */
:deep(.el-message-box) {
  z-index: v-bind('Z_INDEX_DIALOG.CONFIRM_DIALOG') !important;
}

:deep(.el-message-box__wrapper) {
  z-index: v-bind('Z_INDEX_DIALOG.CONFIRM_DIALOG_WRAPPER') !important;
}

:deep(.el-overlay.is-message-box) {
  z-index: v-bind('Z_INDEX_DIALOG.CONFIRM_DIALOG_OVERLAY') !important;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .terms-dialog-content {
    max-height: 50vh;
  }
  
  .term-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>