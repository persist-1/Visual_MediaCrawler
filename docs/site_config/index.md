---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "Visual_MediaCrawler"
  text: "可视化媒体爬虫"
  tagline: 支持：哔哩哔哩 | 抖音 | 小红书 | 贴吧 | 微博 | 知乎 | 快手；根据：关键词 | 详情页 | 创作者 进行爬取 （Based on 'MediaCrawler')
  # image:
  #   src: ./images/logo1.svg
  #   alt: Visual_MediaCrawler
    # 打包时路径为images，不再使用public/images，不知道为什么index页面和其它md页面的打包逻辑不一样...
  actions:
    - theme: brand
      text: 使用说明
      link: /1.使用说明
    - theme: brand
      text: 前端展示
      link: https://visual-mediacrawler-frontend.pages.dev/ 
    - theme: alt
      text: 免责声明
      link: /7.项目免责声明
    - theme: alt
      text: 源项目"MediaCrawler"
      link: https://github.com/NanmiCoder/MediaCrawler

features:
  - icon: 👁️
    title: 多个主流媒体平台支持
    details: 支持哔哩哔哩、抖音、小红书、贴吧、微博、知乎、快手等多个媒体平台，用户可以根据关键词、详情页链接、创作者id进行数据爬取。
  - icon: 🔧
    title: 高性能 API 服务
    details: 使用 FastAPI 构建了支持异步高并发的 API 服务器，所有功能均可通过 API 接口进行调用，提升了系统的可扩展性和集成能力。
  - icon: 🔗
    title: 多个关系性数据库
    details: 增加了 SQLite 数据库作为默认存储数据库，并编写了相应的数据库事务脚本，以兼容 MySQL 存储。同时，这种设计也更利于对其他关系型数据库的适配，为用户提供了更多数据存储选择。
  - icon: 🖥️
    title: 直观的用户界面
    details: 构建了前端服务，提供了 "数据爬取" 和 "数据展示" 两个核心界面，使得操作更加便捷直观，充分对齐了项目的核心功能，提升了用户体验。
  - icon: 🤖
    title: AI开发
    details: 70%+的改动代码是通过AI编程实现的，包括但不限于：数据爬取、数据清洗、数据存储、数据展示等。
---

