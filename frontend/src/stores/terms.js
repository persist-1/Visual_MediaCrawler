import { defineStore } from 'pinia'

export const useTermsStore = defineStore('terms', {
  state: () => ({
    // 条款确认状态
    termsAccepted: false,
    // 已确认的条款列表
    acceptedTerms: [],
    // 条款列表
    termsOfUse: [
      {
        id: 'MCorigin',
        title: '需同意MediaCrawler的作者的所有条款',
        content: `源项目MediaCrawler的免责声明

1. 项目目的与性质
本项目（以下简称"本项目"）是作为一个技术研究与学习工具而创建的，旨在探索和学习网络数据采集技术。本项目专注于自媒体平台的数据爬取技术研究，旨在提供给学习者和研究者作为技术交流之用。

2. 法律合规性声明
本项目开发者（以下简称"开发者"）郑重提醒用户在下载、安装和使用本项目时，严格遵守中华人民共和国相关法律法规，包括但不限于《中华人民共和国网络安全法》、《中华人民共和国反间谍法》等所有适用的国家法律和政策。用户应自行承担一切因使用本项目而可能引起的法律责任。

3. 使用目的限制
本项目严禁用于任何非法目的或非学习、非研究的商业行为。本项目不得用于任何形式的非法侵入他人计算机系统，不得用于任何侵犯他人知识产权或其他合法权益的行为。用户应保证其使用本项目的目的纯属个人学习和技术研究，不得用于任何形式的非法活动。

4. 免责声明
开发者已尽最大努力确保本项目的正当性及安全性，但不对用户使用本项目可能引起的任何形式的直接或间接损失承担责任。包括但不限于由于使用本项目而导致的任何数据丢失、设备损坏、法律诉讼等。

5. 知识产权声明
本项目的知识产权归开发者所有。本项目受到著作权法和国际著作权条约以及其他知识产权法律和条约的保护。用户在遵守本声明及相关法律法规的前提下，可以下载和使用本项目。

6. 最终解释权
关于本项目的最终解释权归开发者所有。开发者保留随时更改或更新本免责声明的权利，恕不另行通知`
      },
      {
        id: 'license',
        title: '开源许可协议遵守',
        content: '该项目的开源许可协议继承源项目"MediaCrawler"的开源许可协议——"NON-COMMERCIAL LEARNING LICENSE 1.1"，必须遵守该项目的开源许可协议和不允许对他人造成利益损失的情况下可使用本项目，严禁使用本项目进行违法犯罪，任何后果自行承担。'
      },
      {
        id: 'compliance',
        title: '数据采集合规性',
        content: '使用本项目进行数据采集时，必须遵守相关平台的服务条款和robots.txt协议，不得进行恶意爬取或对目标网站造成过大负载，违反该条例以及相关法律规定所造成的后果自行承担。'
      },
      {
        id: 'privacy',
        title: '个人信息保护',
        content: '在采集和处理数据时，必须严格遵守《中华人民共和国个人信息保护法》等相关法律法规，不得非法收集、使用、传播他人个人信息。违反该条例以及相关法律规定所造成的后果自行承担。'
      },
      {
        id: 'disclaimer',
        title: '免责声明',
        content: '使用本项目所产生的任何法律风险和后果均由使用者自行承担，项目开发者和贡献者不承担任何直接或间接的法律责任。'
      },
      
    ]
  }),

  getters: {
    // 检查是否所有条款都已确认
    allTermsAccepted: (state) => {
      return state.termsOfUse.length > 0 && 
             state.acceptedTerms.length === state.termsOfUse.length &&
             state.termsOfUse.every(term => state.acceptedTerms.includes(term.id))
    },
    
    // 获取未确认的条款
    unacceptedTerms: (state) => {
      return state.termsOfUse.filter(term => !state.acceptedTerms.includes(term.id))
    },
    
    // 获取已确认的条款详情
    acceptedTermsDetails: (state) => {
      return state.termsOfUse.filter(term => state.acceptedTerms.includes(term.id))
    }
  },

  actions: {
    // 初始化条款状态（从localStorage读取）
    initTermsState() {
      try {
        const savedState = localStorage.getItem('visual_mediacrawler_terms')
        if (savedState) {
          const parsed = JSON.parse(savedState)
          this.acceptedTerms = parsed.acceptedTerms || []
          this.termsAccepted = this.allTermsAccepted
        }
      } catch (error) {
        console.error('读取条款状态失败:', error)
        this.resetTermsState()
      }
    },
    
    // 确认单个条款
    acceptTerm(termId) {
      if (!this.acceptedTerms.includes(termId)) {
        this.acceptedTerms.push(termId)
        this.updateTermsAccepted()
        this.saveTermsState()
      }
    },
    
    // 取消确认单个条款
    rejectTerm(termId) {
      const index = this.acceptedTerms.indexOf(termId)
      if (index > -1) {
        this.acceptedTerms.splice(index, 1)
        this.saveTermsState()
        this.updateTermsAccepted()
      }
    },
    
    // 确认所有条款
    acceptAllTerms() {
      this.acceptedTerms = this.termsOfUse.map(term => term.id)
      this.saveTermsState()
      this.updateTermsAccepted()
    },
    
    // 重置所有条款状态
    resetTermsState() {
      this.acceptedTerms = []
      this.termsAccepted = false
      this.saveTermsState()
    },
    
    // 更新总体确认状态
    updateTermsAccepted() {
      this.termsAccepted = this.allTermsAccepted
    },
    
    // 保存状态到localStorage
    saveTermsState() {
      try {
        const stateToSave = {
          acceptedTerms: this.acceptedTerms,
          timestamp: new Date().toISOString()
        }
        localStorage.setItem('visual_mediacrawler_terms', JSON.stringify(stateToSave))
      } catch (error) {
        console.error('保存条款状态失败:', error)
      }
    },
    
    // 检查条款是否已确认
    isTermAccepted(termId) {
      return this.acceptedTerms.includes(termId)
    }
  }
})