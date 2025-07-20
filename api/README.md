# MediaCrawler API 服务

这是一个基于 FastAPI 的 MediaCrawler API 服务，提供了与命令行工具相同的功能，但通过 HTTP API 接口进行调用。

## 🚀 快速开始

### 安装依赖

```bash
# 进入 api 目录
cd api

```

### 启动服务

```bash
# 使用 uvicorn 启动
uvicorn api:app --host 0.0.0.0 --port 10001 --reload
```



## 📋 API 接口说明

### 1. 同步执行爬虫任务

**接口**: `POST /crawler/run`

**描述**: 同步执行爬虫任务，等待任务完成后返回结果

**请求示例**:
```json
{
  "platform": "xhs",
  "lt": "qrcode",
  "type": "detail",
  "keywords": "编程副业",
  "get_comment": true,
  "save_data_option": "json"
}
```

### 2. 异步执行爬虫任务

**接口**: `POST /crawler/run-async`

**描述**: 异步执行爬虫任务，立即返回任务ID，任务在后台执行

**请求示例**:
```json
{
  "platform": "xhs",
  "lt": "qrcode",
  "type": "search",
  "keywords": "编程兼职",
  "get_comment": false,
  "save_data_option": "csv"
}
```

**响应示例**:
```json
{
  "success": true,
  "message": "爬虫任务已提交，正在后台执行",
  "task_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 3. 查询任务状态

**接口**: `GET /crawler/task/{task_id}`

**描述**: 查询异步任务的执行状态

**响应示例**:
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "message": "任务执行成功",
  "result": {
    "stdout": "爬虫执行日志...",
    "stderr": ""
  }
}
```

### 4. 获取所有任务列表

**接口**: `GET /crawler/tasks`

**描述**: 获取所有任务的列表和状态

### 5. 删除任务记录

**接口**: `DELETE /crawler/task/{task_id}`

**描述**: 删除指定的任务记录

## 📝 请求参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| platform | string | 否 | "xhs" | 媒体平台选择 (xhs\|dy\|ks\|bili\|wb\|tieba\|zhihu) |
| lt | string | 否 | "qrcode" | 登录类型 (qrcode\|phone\|cookie) |
| type | string | 否 | "search" | 爬虫类型 (search\|detail\|creator) |
| start | integer | 否 | null | 起始页数 |
| keywords | string | 否 | null | 搜索关键词 |
| get_comment | boolean | 否 | null | 是否爬取一级评论 |
| get_sub_comment | boolean | 否 | null | 是否爬取二级评论 |
| save_data_option | string | 否 | "json" | 数据保存方式 (csv\|db\|json) |
| cookies | string | 否 | null | 用于cookie登录类型的cookies |

## 🔧 使用示例

### Python 客户端示例

```python
import requests
import time

# API 基础地址
base_url = "http://localhost:10001"

# 1. 同步执行爬虫任务
def sync_crawl():
    data = {
        "platform": "xhs",
        "lt": "qrcode",
        "type": "detail",
        "keywords": "编程副业",
        "get_comment": True,
        "save_data_option": "json"
    }
    
    response = requests.post(f"{base_url}/crawler/run", json=data)
    result = response.json()
    
    if result["success"]:
        print("爬虫任务执行成功")
        print(result["data"]["stdout"])
    else:
        print(f"爬虫任务执行失败: {result['message']}")

# 2. 异步执行爬虫任务
def async_crawl():
    data = {
        "platform": "xhs",
        "lt": "qrcode",
        "type": "search",
        "keywords": "编程兼职",
        "get_comment": False,
        "save_data_option": "csv"
    }
    
    # 提交任务
    response = requests.post(f"{base_url}/crawler/run-async", json=data)
    result = response.json()
    
    if result["success"]:
        task_id = result["task_id"]
        print(f"任务已提交，任务ID: {task_id}")
        
        # 轮询任务状态
        while True:
            status_response = requests.get(f"{base_url}/crawler/task/{task_id}")
            status_result = status_response.json()
            
            print(f"任务状态: {status_result['status']} - {status_result['message']}")
            
            if status_result["status"] in ["completed", "failed"]:
                if status_result["result"]:
                    print("执行结果:")
                    print(status_result["result"]["stdout"])
                break
            
            time.sleep(5)  # 等待5秒后再次查询
    else:
        print(f"任务提交失败: {result['message']}")

if __name__ == "__main__":
    # 选择执行方式
    # sync_crawl()  # 同步执行
    async_crawl()   # 异步执行
```

### cURL 示例

```bash
# 1. 健康检查
curl -X GET "http://localhost:10001/health"

# 2. 同步执行爬虫任务
curl -X POST "http://localhost:10001/crawler/run" \
     -H "Content-Type: application/json" \
     -d '{
       "platform": "xhs",
       "lt": "qrcode",
       "type": "detail",
       "keywords": "编程副业",
       "get_comment": true,
       "save_data_option": "json"
     }'

# 3. 异步执行爬虫任务
curl -X POST "http://localhost:10001/crawler/run-async" \
     -H "Content-Type: application/json" \
     -d '{
       "platform": "xhs",
       "lt": "qrcode",
       "type": "search",
       "keywords": "编程兼职",
       "get_comment": false,
       "save_data_option": "csv"
     }'

# 4. 查询任务状态（替换 {task_id} 为实际的任务ID）
curl -X GET "http://localhost:10001/crawler/task/{task_id}"

# 5. 获取所有任务列表
curl -X GET "http://localhost:10001/crawler/tasks"
```

## 🔍 注意事项

1. **环境要求**: 确保已经按照主项目的要求安装了所有依赖（uv、playwright等）
2. **工作目录**: API 服务会在项目根目录下执行 `uv run main.py` 命令
3. **登录状态**: 如果使用二维码登录，需要在命令行中手动扫码
4. **任务管理**: 异步任务的状态信息存储在内存中，服务重启后会丢失
5. **并发限制**: 建议不要同时执行过多的爬虫任务，以免对目标平台造成压力

## 🚀 快速启动

### 方式一：使用启动脚本（推荐）
```bash
# 基本启动
python start_api.py

# 自定义端口和地址
python start_api.py --host 0.0.0.0 --port 8080

# 开发模式（热重载）
python start_api.py --dev

# 查看所有选项
python start_api.py --help
```

### 方式二：使用 Docker
```bash
# 构建并启动服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f mediacrawler-api

# 停止服务
docker-compose down
```

### 方式三：使用自动化部署脚本
```bash
# 本地开发部署
python deploy.py local --start --dev

# Docker 部署
python deploy.py docker --build --detach

# 生产环境部署（需要 sudo 权限）
python deploy.py production --port 10001 --start
```

### 方式四：直接使用 uvicorn
```bash
uvicorn api:app --host 0.0.0.0 --port 10001 --reload
```

## ⚙️ 配置说明

### 基础配置
1. 复制配置文件模板：
```bash
cp config.example.py config.py
```

2. 根据需要修改 `config.py` 中的配置项：
   - API 服务配置（端口、日志等）
   - 任务管理配置（并发数、超时等）
   - 安全配置（API密钥、CORS等）
   - 数据库配置（如果需要持久化任务状态）

### Docker 配置
- `Dockerfile`: 容器镜像构建配置
- `docker-compose.yml`: 完整服务栈配置，包含：
  - MediaCrawler API 服务
  - Redis 缓存服务（可选）
  - MySQL 数据库服务（可选）



## 🛠️ 开发说明

### 项目结构
```
api/
├── api.py                 # FastAPI 应用主文件
├── test_client.py        # 测试客户端
└── README.md            # 本文档
```

### 扩展功能

- ✅ 任务状态管理和查询
- ✅ 异步任务执行
- ✅ Docker 容器化部署
- ✅ 配置文件管理
- 🔄 用户认证和权限控制
- 🔄 任务队列和分布式处理
- 🔄 数据可视化界面
- 🔄 监控和日志系统
- 🔄 更多数据格式导出

### 性能优化建议
1. **并发控制**：根据服务器性能调整 `max_concurrent_tasks`
2. **资源监控**：启用监控功能，观察CPU和内存使用情况
3. **数据库优化**：如果使用数据库存储，建议使用 MySQL 或 PostgreSQL
4. **缓存策略**：启用 Redis 缓存，提高响应速度
5. **负载均衡**：生产环境建议使用 Nginx 进行负载均衡

## 📄 许可证

本项目遵循与主项目相同的许可证条款，仅供学习和研究使用。