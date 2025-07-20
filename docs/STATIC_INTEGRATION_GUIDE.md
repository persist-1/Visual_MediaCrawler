# Visual_MediaCrawler 静态文件集成指南

## 概述

本指南介绍了如何使用新增的 `static_page_api.py` 模块，实现前后端一体化部署。通过这个模块，FastAPI 服务器可以同时提供后端 API 服务和前端静态文件服务，使得整个应用可以通过单一端口访问。

## 功能特性

### 1. 静态文件服务
- **前端资源托管**: 自动托管 `frontend/dist` 目录下的所有静态文件
- **SPA 路由支持**: 为单页应用提供路由支持，所有前端路由都返回 `index.html`
- **资源优化**: 自动处理 CSS、JS、图片等静态资源的访问
- **CORS 配置**: 内置 CORS 中间件，支持跨域请求

### 2. 智能检测
- **前端文件检测**: 自动检测前端构建文件是否存在
- **优雅降级**: 当前端文件不存在时，仍可正常提供 API 服务
- **状态监控**: 提供静态服务状态检查端点

### 3. 开发友好
- **热重载支持**: 开发模式下支持前后端热重载
- **调试信息**: 详细的日志输出，便于调试
- **灵活配置**: 支持自定义前端构建路径

## 文件结构

```
Visual_MediaCrawler/
├── api/
│   ├── api.py                 # 主API服务（已集成静态服务）
│   ├── static_page_api.py     # 静态文件服务模块
│   └── extra_sqlite_api.py    # 数据库API
├── frontend/
│   ├── dist/                  # 前端构建输出目录
│   │   ├── index.html         # 前端入口文件
│   │   ├── assets/            # 静态资源目录
│   │   └── vite.svg           # 其他静态文件
│   ├── src/                   # 前端源码
│   └── package.json           # 前端依赖配置
└── test_static_integration.py # 集成测试脚本
```

## 使用方法

### 1. 基本使用

静态文件服务已经集成到主 API 服务中，无需额外配置：

```bash
# 启动集成服务
cd d:\A_work\A_trae_alter\Visual_MediaCrawler
python api/api.py
```

服务启动后，可以通过以下地址访问：
- **前端应用**: http://localhost:10001/
- **API 服务**: http://localhost:10001/api
- **API 文档**: http://localhost:10001/docs
- **静态服务状态**: http://localhost:10001/static/status

### 2. 前端构建

在使用静态文件服务之前，需要先构建前端项目：

```bash
# 进入前端目录
cd frontend

# 安装依赖（如果还没有安装）
npm install

# 构建前端项目
npm run build
```

构建完成后，会在 `frontend/dist` 目录生成静态文件。

### 3. 开发模式

开发模式下，可以同时运行前后端服务：

```bash
# 终端1：启动后端服务
cd d:\A_work\A_trae_alter\Visual_MediaCrawler
python api/api.py

# 终端2：启动前端开发服务（可选）
cd frontend
npm run dev
```

## API 路由说明

### 静态文件路由

| 路由 | 描述 | 返回内容 |
|------|------|----------|
| `/` | 前端根页面 | index.html |
| `/crawler` | 爬虫页面 | index.html (SPA路由) |
| `/data` | 数据展示页面 | index.html (SPA路由) |
| `/settings` | 设置页面 | index.html (SPA路由) |
| `/about` | 关于页面 | index.html (SPA路由) |
| `/assets/*` | 静态资源 | CSS/JS/图片等文件 |
| `/vite.svg` | 图标文件 | SVG图标 |

### API 服务路由

| 路由 | 描述 | 方法 |
|------|------|------|
| `/api` | API根路径 | GET |
| `/health` | 健康检查 | GET |
| `/static/status` | 静态服务状态 | GET |
| `/docs` | API文档 | GET |
| `/crawler/*` | 爬虫相关API | GET/POST/DELETE |
| `/sqlite/*` | 数据库相关API | GET |

## 配置选项

### 1. 自定义前端路径

```python
from fastapi import FastAPI
from static_page_api import create_integrated_app

app = FastAPI()

# 使用自定义前端路径
integrated_app = create_integrated_app(
    app, 
    frontend_dist_path="/path/to/custom/dist"
)
```

### 2. CORS 配置

```python
from static_page_api import setup_static_page_api

app = FastAPI()
static_api = setup_static_page_api(app)

# 自定义CORS配置
static_api.setup_cors(
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"]
)
```

## 测试验证

### 1. 运行集成测试

```bash
# 运行自动化测试
python test_static_integration.py
```

测试脚本会自动：
- 启动API服务器
- 测试所有API端点
- 验证静态文件服务
- 检查前端路由
- 测试API文档访问

### 2. 手动测试

1. **启动服务**:
   ```bash
   python api/api.py
   ```

2. **访问前端**: 打开浏览器访问 http://localhost:10001/

3. **测试API**: 访问 http://localhost:10001/docs 查看API文档

4. **检查状态**: 访问 http://localhost:10001/static/status 查看静态服务状态

## 故障排除

### 1. 前端页面无法访问

**问题**: 访问根路径返回404或错误

**解决方案**:
- 检查 `frontend/dist` 目录是否存在
- 确认 `frontend/dist/index.html` 文件存在
- 运行 `npm run build` 重新构建前端

### 2. 静态资源加载失败

**问题**: CSS/JS文件无法加载

**解决方案**:
- 检查 `frontend/dist/assets` 目录是否存在
- 确认前端构建配置正确
- 检查浏览器开发者工具的网络面板

### 3. API路由冲突

**问题**: API路由被静态路由覆盖

**解决方案**:
- API路由现在使用 `/api` 前缀
- 确保前端路由不与API路由冲突
- 检查路由注册顺序

### 4. CORS错误

**问题**: 跨域请求被阻止

**解决方案**:
- 检查CORS配置
- 确认允许的源地址正确
- 在开发环境中可以使用 `allow_origins=["*"]`

## 部署建议

### 1. 生产环境

```python
# 生产环境配置示例
from static_page_api import create_integrated_app

app = FastAPI()
integrated_app = create_integrated_app(app)

# 限制CORS源
static_api.setup_cors(
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True
)

# 使用生产级WSGI服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        workers=4
    )
```

### 2. Docker部署

```dockerfile
FROM python:3.13-slim

# 安装Node.js用于构建前端
RUN apt-get update && apt-get install -y nodejs npm

WORKDIR /app

# 复制项目文件
COPY . .

# 安装Python依赖
RUN pip install -r requirements.txt

# 构建前端
RUN cd frontend && npm install && npm run build

# 启动服务
CMD ["python", "api/api.py"]
```

### 3. 反向代理

如果使用Nginx等反向代理，建议配置：

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    # 静态文件直接由Nginx服务（可选优化）
    location /assets/ {
        alias /path/to/app/frontend/dist/assets/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # API请求转发到FastAPI
    location /api/ {
        proxy_pass http://localhost:10001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # 其他请求转发到FastAPI（包括前端路由）
    location / {
        proxy_pass http://localhost:10001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 最佳实践

1. **开发阶段**: 使用前后端分离模式，便于调试
2. **测试阶段**: 使用集成模式，验证完整功能
3. **生产部署**: 使用集成模式，简化部署流程
4. **性能优化**: 在反向代理层处理静态文件缓存
5. **安全考虑**: 限制CORS源，使用HTTPS

## 更新日志

- **v1.0.0**: 初始版本，支持基本静态文件服务
- **v1.1.0**: 添加SPA路由支持
- **v1.2.0**: 增加智能检测和状态监控
- **v1.3.0**: 优化CORS配置和错误处理

## 技术支持

如果在使用过程中遇到问题，请：

1. 查看本文档的故障排除部分
2. 运行 `test_static_integration.py` 进行诊断
3. 检查服务器日志输出
4. 访问 `/static/status` 端点查看服务状态

---

**注意**: 本功能为 Visual_MediaCrawler 项目的增强功能，旨在简化部署流程和提升用户体验。在生产环境中使用时，请确保进行充分的测试。