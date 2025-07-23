import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Visual_MediaCrawler",
  description: "可视化爬虫（支持：哔哩哔哩 | 抖音 | 小红书 | 贴吧 | 微博 | 知乎 | 快手），异步、高效、直观地采集国内主流平台的媒体数据的前后端一体项目（Based on \"MediaCrawler\"）。",
  base: '/Visual_MediaCrawler/',
  
  // 忽略死链接检查
  ignoreDeadLinks: true,

  head: [
      // 添加图标
      ['link', { rel: 'icon', type: 'image/svg+xml', href: '/Visual_MediaCrawler/static/images/logo.svg' }]
    ],

  themeConfig: {

    logo: '/Visual_MediaCrawler/static/images/logo.svg',
    siteTitle: 'Visual_MediaCrawler | 项目文档',

    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: '项目文档', link: '/README' },
      { text: '免责声明', link: '/7.免责声明' }
    ],

    sidebar: [
      {
        text: '文档说明',
        items: [
          { text: '1.使用说明', link: '/1.使用说明' },
          { text: '2.数据库初始化指南', link: '/2.数据库初始化指南' },
          { text: '3.项目代码结构', link: '/3.项目代码结构' },
          { text: '4.API接口文档', link: '/4.API接口文档' },
          { text: '5.项目环境管理与搭建', link: '/5.项目环境管理指南' },
          { text: '6.存在问题与未来计划', link: '/6.存在问题-未来计划' },
          { text: '7.项目免责声明', link: '/7.免责声明' },
          { text: '8.项目开源协议', link: '/8.开源协议' },
          { text: '本项目README', link: '/README' },
          { text: '源项目README', link: '/Origin_README' },
        ]
      }
  
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/persist-1/Visual_MediaCrawler' }
    ],

    // 站点页脚配置
    footer: {
      message: "Released under the 'NON-COMMERCIAL LEARNING LICENSE 1.1' License",
      copyright: "Copyright © 2025-present persist-1",
    },
  }
})
