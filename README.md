# Visual_MediaCrawler

本项目名为 "Visual_MediaCrawler"，是一个前后端分离的媒体数据采集平台。它能够异步、高效、直观地采集国内主流平台的媒体数据，并将其存储在本地 SQLite 数据库中。用户可以根据需求筛选和导出 CSV/JSON 格式的数据，以便进行数据分析和提供给 BI 工具使用。

本项目基于知名的开源项目 "MediaCrawler" (https://github.com/NanmiCoder/MediaCrawler) 进行了大幅度改进，主要改进内容如下：

1. **高性能 API 服务**：使用 FastAPI 构建了支持异步高并发的 API 服务器，所有功能均可通过 API 接口进行调用，提升了系统的可扩展性和集成能力。
2. **灵活的数据库支持**：增加了 SQLite 数据库作为默认存储数据库，并编写了相应的数据库事务脚本，以兼容 MySQL 存储。同时，这种设计也更利于对其他关系型数据库的适配，为用户提供了更多数据存储选择。
3. **直观的用户界面**：构建了前端服务，提供了 "数据爬取" 和 "数据展示" 两个核心界面，使得操作更加便捷直观，充分对齐了项目的核心功能，提升了用户体验。
4. **现代化开发环境**：使用 `uv` 管理项目环境，并将 Python 版本升级到 3.13.5。同时，同步升级了所有依赖包以适配新版本，并对过时的代码进行了更新，确保了项目的稳定性和前瞻性。
5. **增强的命令行与功能**：对命令行工具及其功能进行了更新，增加了以下新参数：
   - `--max_count`：用于控制单次爬取的上限条数。
   - `--task_id`：引入了 "任务(每次)ID" 的概念，以 "每次任务" 为数据管理理念，并适配了 API 服务，方便用户追踪和管理每次爬取任务。
   - `--sync_to_mysql`：支持将爬取结果同步至 MySQL 数据库，且该存储进程独立于 SQLite 存储，提供了更多数据同步的灵活性。

## 项目结构

```
Visual_MediaCrawler/
├── api/                     # FastAPI 应用主文件和API相关逻辑
│   ├── api.py              # 主API服务文件
│   ├── extra_sqlite_api.py # SQLite数据库API扩展
│   ├── api_run.bat         # API服务启动脚本
│   └── README.md           # API服务说明文档
├── async_db.py              # 异步 MySQL 数据库操作封装
├── async_sqlite_db.py       # 异步 SQLite 数据库操作封装
├── base/                    # 基础爬虫模块
│   └── base_crawler.py     # 爬虫基类
├── browser_data/            # 浏览器用户数据目录（仅爬取进行时产生并存在）
├── cache/                   # 缓存模块
│   ├── abs_cache.py        # 抽象缓存类
│   ├── cache_factory.py    # 缓存工厂
│   ├── local_cache.py      # 本地缓存实现
│   └── redis_cache.py      # Redis缓存实现
├── cmd_arg/                 # 命令行参数处理
│   └── arg.py              # 参数解析器
├── config/                  # 项目配置，包括数据库配置、基础配置等
│   ├── base_config.py      # 基础配置
│   └── db_config.py        # 数据库配置
├── constant/                # 常量定义
│   ├── baidu_tieba.py      # 百度贴吧常量
│   └── zhihu.py            # 知乎常量
├── data/                    # 爬取数据存储目录
│   ├── bilibili/           # B站数据
│   └── douyin/             # 抖音数据
├── db.py                    # 数据库初始化和管理
├── debug_tools/             # 调试工具
│   ├── create_db.py        # 数据库创建工具
│   ├── db_analyzer.py      # 数据库分析工具
│   └── quick_analyze.py    # 快速分析工具
├── docs/                    # 文档和资源文件
│   ├── .vitepress/         # VitePress文档配置
│   ├── static/             # 静态资源
│   └── *.md                # 各种说明文档
├── frontend/                # 前端服务代码
│   ├── src/                # 前端源码
│   │   ├── api/            # API接口封装
│   │   ├── components/     # Vue组件
│   │   └── views/          # 页面视图
│   ├── public/             # 静态资源
│   ├── index.html          # 入口HTML文件
│   ├── package.json        # 前端依赖配置
│   ├── vite.config.js      # Vite配置
│   └── frontend_run_dev.bat # 前端开发服务启动脚本
├── libs/                    # 第三方库或自定义工具库
│   ├── douyin.js           # 抖音相关JS库
│   ├── stealth.min.js      # 反检测库
│   └── zhihu.js            # 知乎相关JS库
├── main.py                  # 爬虫主入口
├── media_platform/          # 各媒体平台爬虫实现
│   ├── bilibili/           # B站爬虫
│   ├── douyin/             # 抖音爬虫
│   ├── kuaishou/           # 快手爬虫
│   ├── tieba/              # 百度贴吧爬虫
│   ├── weibo/              # 微博爬虫
│   ├── xhs/                # 小红书爬虫
│   └── zhihu/              # 知乎爬虫
├── model/                   # 数据模型定义
│   ├── m_baidu_tieba.py    # 百度贴吧数据模型
│   ├── m_douyin.py         # 抖音数据模型
│   ├── m_kuaishou.py       # 快手数据模型
│   ├── m_weibo.py          # 微博数据模型
│   ├── m_xiaohongshu.py    # 小红书数据模型
│   └── m_zhihu.py          # 知乎数据模型
├── proxy/                   # 代理相关配置和实现
│   ├── base_proxy.py       # 代理基类
│   ├── providers/          # 代理提供商
│   ├── proxy_ip_pool.py    # 代理IP池
│   └── types.py            # 代理类型定义
├── schema/                  # 数据库表结构定义
│   ├── mc.db               # 主数据库文件
│   ├── sqlite_tables.db    # SQLite表结构数据库
│   ├── sqlite_tables.sql   # SQLite表结构SQL
│   └── tables.sql          # 表结构SQL
├── store/                   # 数据存储逻辑
│   ├── bilibili/           # B站数据存储
│   ├── douyin/             # 抖音数据存储
│   ├── kuaishou/           # 快手数据存储
│   ├── tieba/              # 百度贴吧数据存储
│   ├── weibo/              # 微博数据存储
│   ├── xhs/                # 小红书数据存储
│   └── zhihu/              # 知乎数据存储
├── test/                    # 测试文件
│   ├── test_expiring_local_cache.py # 本地缓存测试
│   ├── test_proxy_ip_pool.py        # 代理池测试
│   ├── test_redis_cache.py          # Redis缓存测试
│   └── test_utils.py                # 工具函数测试
├── tools/                   # 通用工具函数
│   ├── browser_launcher.py # 浏览器启动器
│   ├── cdp_browser.py      # CDP浏览器控制
│   ├── crawler_util.py     # 爬虫工具
│   ├── easing.py           # 缓动函数
│   ├── slider_util.py      # 滑块验证工具
│   ├── time_util.py        # 时间工具
│   ├── utils.py            # 通用工具
│   └── words.py            # 词汇处理
├── var.py                   # 全局变量
├── .gitattributes          # Git属性配置
├── .github/                 # GitHub Actions 配置
├── .gitignore              # Git忽略文件配置
├── .python-version          # Python 版本管理
├── .venv/                   # Python 虚拟环境
├── LICENSE                  # 项目许可证
├── Origin_README.md         # 原始 README 文件
├── mypy.ini                 # Mypy 配置
├── package-lock.json        # 前端依赖锁定文件
├── package.json             # 前端项目配置
├── pyproject.toml           # 项目依赖和元数据
├── recv_sms.py              # 短信接收相关脚本
├── requirements.txt         # Python 依赖列表
├── uv.lock                  # uv 锁文件
└── README.md                # 项目说明文档
```

## 后端 API 接口列表

### 爬虫任务管理接口

- **GET /**：API根路径，返回服务状态信息
- **POST /crawler/run**：同步执行爬虫任务，等待任务完成后返回结果
- **POST /crawler/run-async**：异步执行爬虫任务，立即返回任务ID，任务在后台执行
- **GET /crawler/task/{task_times_id}**：查询指定任务的执行状态和结果
- **GET /crawler/tasks**：获取所有任务的列表和状态信息
- **DELETE /crawler/task/{task_times_id}**：删除指定任务的记录
- **GET /health**：健康检查接口，用于监控API服务状态

### SQLite 数据管理接口

- **GET /sqlite/tables**：获取所有可用的 SQLite 数据表列表
- **GET /sqlite/data**：获取指定 SQLite 表格的数据，支持分页和任务 ID 筛选
- **GET /sqlite/stats**：获取 SQLite 数据库的统计信息，包括总数据量、表数量、今日新增和最新更新时间
- **GET /sqlite/export**：导出指定 SQLite 表格的数据为 CSV 格式
- **GET /sqlite/export-json**：导出指定 SQLite 表格的数据为 JSON 格式
- **GET /sqlite/configs**：获取所有数据表的配置信息，包括字段定义和显示配置

### 支持的平台

本项目支持以下主流媒体平台的数据采集：

- **小红书 (xhs)**：支持搜索、详情页、创作者数据采集
- **抖音 (dy)**：支持视频搜索、详情页、创作者数据采集
- **快手 (ks)**：支持视频搜索、详情页、创作者数据采集
- **哔哩哔哩 (bili)**：支持视频搜索、详情页、UP主数据采集
- **微博 (wb)**：支持微博搜索、详情页、用户数据采集
- **百度贴吧 (tieba)**：支持帖子搜索、详情页数据采集
- **知乎 (zhihu)**：支持问答搜索、详情页、用户数据采集

### 登录方式

- **二维码登录 (qrcode)**：通过扫描二维码进行登录
- **手机号登录 (phone)**：使用手机号和验证码登录
- **Cookie登录 (cookie)**：使用已有的Cookie信息登录

### 数据存储

- **SQLite 数据库**：默认存储方式，轻量级本地数据库
- **MySQL 数据库**：可选的数据同步方式，支持企业级数据存储
- **CSV/JSON 导出**：支持将数据导出为常见的数据格式，便于数据分析

## 快速开始

### 环境要求

- Python 3.13.5+
- Node.js 16+
- uv (Python包管理器)

### 安装依赖

```bash
# 安装Python依赖
uv sync

# 安装前端依赖
cd frontend
npm install
```

### 启动服务

```bash
# 启动后端API服务
cd api
python api.py

# 启动前端开发服务
cd frontend
npm run dev
```

### 使用说明

1. 访问前端界面进行可视化操作
2. 或直接调用API接口进行数据采集
3. 查看SQLite数据库中的采集结果
4. 根据需要导出CSV或JSON格式的数据

## 技术特性

- **异步高并发**：基于FastAPI和asyncio实现高性能数据采集
- **模块化设计**：清晰的项目结构，易于维护和扩展
- **多平台支持**：覆盖国内主流媒体平台
- **灵活的数据存储**：支持SQLite和MySQL双重存储
- **任务管理**：完整的任务生命周期管理
- **数据导出**：多种格式的数据导出功能
- **前端可视化**：直观的Web界面操作

## 许可证

本项目基于开源许可证发布，仅供学习和研究目的使用。使用时请遵守相关平台的使用条款和robots.txt规则，合理控制请求频率，避免对目标平台造成不必要的负担。

## 贡献

欢迎提交Issue和Pull Request来帮助改进项目。在贡献代码前，请确保遵循项目的代码规范和最佳实践。