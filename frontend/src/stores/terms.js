import { defineStore } from 'pinia'

export const useTermsStore = defineStore('terms', {
  state: () => ({
    // 条款确认状态
    termsAccepted: false,
    // 已确认的条款列表
    acceptedTerms: [],
    // 条款列表
    termsOfUse : [
        {
          id: '1MCorigin',
          title: '条款1：必须遵守源项目条款',
          content: `本项目继承了源项目"MediaCrawler"的全部条款，用户必须严格遵守源项目"MediaCrawler"的全部条款以及本项目的全部条款，包括但不限于：
      1. 本项目仅限于技术研究与学习目的，禁止商业使用
      2. 用户需自行承担使用本项目产生的所有法律责任
      3. 禁止用于非法侵入计算机系统或侵犯知识产权等违法犯罪用途
      4. 开发者保留对本项目的最终解释权及修改权`
        },
        {
          id: '2license',
          title: '条款2：开源许可协议遵守',
          content: `用户必须遵守"NON-COMMERCIAL LEARNING LICENSE 1.1"开源协议(继承自源项目"MediaCrawler")：
非商业学习使用许可证 1.1

版权所有 (c) [2025] [persist1@126.com]

鉴于：
1. 版权所有者拥有和控制本软件和相关文档文件（以下简称“软件”）的版权；
2. 使用者希望使用该软件进行学习；
3. 版权所有者愿意在本许可证所述的条件下授权使用者使用该软件；

现因此，双方遵循相关法律法规，同意如下条款：

授权范围：
1. 版权所有者特此免费授予接受本许可证的任何自然人或法人（以下简称“使用者”）非独占的、不可转让的权利，在非商业学习目的下使用、复制、修改、合并本软件，前提是遵守以下条件。

条件：
1. 使用者必须在软件及其副本的所有合理显著位置包含上述版权声明和本许可证声明。
2. 本软件仅限用于学习和研究目的，不得用于大规模爬虫或对平台造成运营干扰的行为。
3. 未经版权所有者书面同意，不得将本软件用于任何商业用途或对第三方造成不当影响。

免责声明：
1. 本软件按“现状”提供，不提供任何形式的明示或暗示保证，包括但不限于对适销性、特定用途的适用性和非侵权的保证。
2. 在任何情况下，版权所有者均不对因使用本软件而产生的，或在任何方式上与本软件有关的任何直接、间接、偶然、特殊、示例性或后果性损害负责（包括但不限于采购替代品或服务；使用、数据或利润的损失；或业务中断），无论这些损害是如何引起的，以及无论是通过合同、严格责任还是侵权行为（包括疏忽或其他方式）产生的，即使已被告知此类损害的可能性。

适用法律：
1. 本许可证的解释和执行应遵循当地法律法规。
2. 因本许可证引起的或与之相关的任何争议，双方应友好协商解决；协商不成时，任何一方可将争议提交至版权所有者所在地的人民法院诉讼解决。

本许可证构成双方之间关于本软件的完整协议，取代并合并以前的讨论、交流和协议，无论是口头还是书面的。`
        },
        {
          id: '3project_nature',
          title: '条款3：项目性质声明',
          content: `1. 本项目为开源项目（许可证类型：NON-COMMERCIAL LEARNING LICENSE 1.1），按"原样"提供
      2. 开发者不提供数据内容服务或商业接口
      3. 开发者不参与用户的数据采集行为
      4. 开发者不存储、处理或分发任何采集数据`
        },
        {
          id: '4prohibited_use',
          title: '条款4：禁止用途',
          content: `用户严禁从事以下行为：
      1. 抓取手机号/身份证号/生物识别信息等敏感个人信息
      2. 采集行踪轨迹、通信内容等隐私数据
      3. 高频访问目标服务器，对目标服务器造成较大压力或导致目标服务器瘫痪
      4. 抓取受著作权保护的作品或商业秘密
      5. 采集涉及国家秘密、军事设施等敏感数据
      6. 修改项目源码以进行违法犯罪活动`
        },
        {
          id: '5user_obligations',
          title: '条款5：用户义务',
          content: `用户必须履行以下义务：
      1. 使用前评估目标网站的Robots协议和用户协议
      2. 不得采集用户的敏感信息和隐私数据（如某平台用户的手机号、身份证号、生物识别信息等）
      3. 遵守《中华人民共和国网络安全法》、《中华人民共和国数据安全法》、《中华人民共和国个人信息保护法》、《中华人民共和国网络安全法》、《中华人民共和国反间谍法》等所有适用的国家法律和政策。用户应自行承担一切因使用本项目而可能引起的法律责任。
      `
        },
        {
          id: '6compliance',
          title: '条款6：数据采集合规性',
          content: `数据采集必须符合以下要求：
      1. 严格遵守各平台服务条款和robots.txt协议
      2. 不得进行恶意爬取或造成目标服务器过载
      3. 不得实质性替代原平台服务
      4. 不得采集《中华人民共和国数据安全法》第32条禁止内容
      5. 因违规造成的法律后果由用户自行承担`
        },
        {
          id: '7privacy',
          title: '条款7：个人信息保护',
          content: `必须严格遵守个人信息保护规范：
      1. 禁止非法收集/使用/传输个人信息（《中华人民共和国个人信息保护法》第10条）
      2. 处理敏感信息需满足法定条件（《中华人民共和国个人信息保护法》第29条）
      3. 使用本项目的源码或修改本项目源码应遵守《中华人民共和国数据安全法》第8、27、28条，妥善处理采集得到的数据`
        },
        {
          id: '8liability',
          title: '条款8：责任限制',
          content: `1. 因用户违规造成的民事赔偿/行政处罚/刑事责任均由用户承担
      2. 开发者不承担任何法律责任，一切法律责任均由用户承担：
      3. 若开发者因用户行为遭受损失（如诉讼费），用户应全额赔偿`
        },
        {
          id: '9intellectual_property',
          title: '条款9：知识产权声明',
          content: `1. 本项目代码版权归开发者所有（《著作权法》第49条）
      2. 用户通过本系统获取的数据，其权利归属及合法性与开发者无关
      3. 禁止任何侵犯著作权的数据抓取行为（如抓取受版权保护的作品）`
        },
        {
          id: '10amendment',
          title: '条款10：协议变更与终止',
          content: `1. 开发者保留单方修改免责声明的权利
      2. 条款更新后通过项目官网或源代码管理平台进行公示，不另行通知
      3. 继续使用视为接受修订条款
      4. 不同意修改内容应立即停止使用并删除代码`
        },
        {
          id: 'jurisdiction',
          title: '条款11：法律管辖',
          content: `1. 本声明适用中华人民共和国法律
      2. 争议提交开发者所在地人民法院诉讼解决
      3. 若条款部分无效，不影响其余条款效力
      4. 最终解释权归开发者所有`
        },
      ]
  }),

  getters: {
    // 检查是否所有条款都已确认
    allTermsAccepted: (state) => {
      if (state.termsOfUse.length === 0) {
        return false
      }
      
      // 检查每个条款是否都已确认
      const allConfirmed = state.termsOfUse.every(term => state.acceptedTerms.includes(term.id))
      
      console.log('allTermsAccepted检查:', {
        termsCount: state.termsOfUse.length,
        acceptedCount: state.acceptedTerms.length,
        allConfirmed,
        termsIds: state.termsOfUse.map(t => t.id),
        acceptedTerms: state.acceptedTerms
      })
      
      return allConfirmed
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
        console.log('条款确认:', {
          termId,
          acceptedTerms: this.acceptedTerms,
          allTermsAccepted: this.allTermsAccepted,
          totalTerms: this.termsOfUse.length
        })
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