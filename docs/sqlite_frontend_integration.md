# SQLite 数据库与前端集成配置指南

## 📋 概述

本文档说明了如何将 SQLite 数据库配置为 MediaCrawler 项目的默认数据存储方式，并与前端服务进行集成。

## 🔧 已完成的配置修改

### 1. 基础配置修改

**文件**: `config/base_config.py`

```python
# 数据存储选项：json, db, csv
SAVE_DATA_OPTION = "db"  # 已修改为数据库存储

# 数据库类型：sqlite, mysql
DB_TYPE = "sqlite"  # 保持SQLite作为默认数据库

# 是否同步数据到MySQL（混合存储模式）
SYNC_TO_MYSQL = False  # 默认关闭MySQL同步
```

### 2. 数据库配置

**文件**: `config/db_config.py`

```python
# SQLite数据库配置
SQLITE_DB_PATH = "data/mc.db"  # 数据库文件路径

# 数据库类型常量
DB_TYPE_SQLITE = "sqlite"
DB_TYPE_MYSQL = "mysql"
```

### 3. 数据库文件位置

- **数据库文件**: `data/mc.db`
- **数据目录**: `data/`
- **表结构定义**: `schema/sqlite_tables.sql`

## 🚀 前端集成说明

### 1. API 服务

**API 服务文件**: `api/api.py`
**API 文档**: `api/README.md`

### 2. 前端服务

**前端目录**: `frontend/`
**配置文件**: `frontend/vite.config.js`
**依赖文件**: `frontend/package.json`

### 3. 服务地址

- **前端服务**: `http://localhost:3000`
- **API 服务**: `http://localhost:8000` (根据vite.config.js配置)

## 📊 支持的数据表

### 平台数据表

1. **B站 (Bilibili)**
   - `bilibili_video` - 视频信息
   - `bilibili_video_comment` - 视频评论
   - `bilibili_up_info` - UP主信息
   - `bilibili_contact_info` - 联系信息
   - `bilibili_up_dynamic` - UP主动态

2. **抖音 (Douyin)**
   - `douyin_aweme` - 视频信息
   - `douyin_aweme_comment` - 视频评论
   - `dy_creator` - 创作者信息

3. **快手 (Kuaishou)**
   - `kuaishou_video` - 视频信息
   - `kuaishou_video_comment` - 视频评论

4. **小红书 (XHS)**
   - `xhs_note` - 笔记信息
   - `xhs_note_comment` - 笔记评论
   - `xhs_creator` - 创作者信息

5. **微博 (Weibo)**
   - `weibo_note` - 微博信息
   - `weibo_note_comment` - 微博评论
   - `weibo_creator` - 创作者信息

6. **贴吧 (Tieba)**
   - `tieba_note` - 帖子信息
   - `tieba_comment` - 帖子评论
   - `tieba_creator` - 创作者信息

7. **知乎 (Zhihu)**
   - `zhihu_content` - 内容信息
   - `zhihu_comment` - 评论信息
   - `zhihu_creator` - 创作者信息

## 🔄 数据流程

### 1. 数据采集流程

```
爬虫采集 → 数据处理 → SQLite存储 → API接口 → 前端展示
```

### 2. 混合存储模式（可选）

```
爬虫采集 → 数据处理 → SQLite存储 + MySQL同步 → API接口 → 前端展示
```

## 🛠️ 使用方法

### 1. 启动服务

```bash
# 启动API服务
python api/api.py

# 启动前端服务（在frontend目录下）
npm run dev
```

### 2. 运行爬虫

```bash
# 运行爬虫（数据将自动保存到SQLite）
python main.py --platform xhs --lt qr_login --type search --keywords 美食
```

### 3. 查看数据

- **前端界面**: 访问 `http://localhost:3000`
- **API接口**: 访问 `http://localhost:8000/docs`
- **数据库文件**: 使用SQLite客户端打开 `data/mc.db`

## 🔍 验证配置

运行验证脚本确认配置正确：

```bash
python verify_sqlite_config.py
```

**预期输出**:
```
🎉 所有验证通过! (5/5)
✅ SQLite 配置正确，可以正常使用
```

## ⚙️ 高级配置

### 1. 启用混合存储模式

在 `config/base_config.py` 中修改：

```python
SYNC_TO_MYSQL = True  # 启用MySQL同步
```

### 2. 自定义数据库路径

在 `config/db_config.py` 中修改：

```python
SQLITE_DB_PATH = "custom/path/database.db"
```

### 3. 性能优化

- **批量插入**: 使用 `execute_many` 方法
- **事务处理**: 在大量数据操作时使用事务
- **索引优化**: 根据查询需求添加索引

## 🚨 注意事项

### 1. 数据安全

- 定期备份 `data/mc.db` 文件
- 避免同时运行多个爬虫实例
- 确保有足够的磁盘空间

### 2. 性能考虑

- SQLite 适合中小规模数据存储
- 大规模数据建议启用混合存储模式
- 定期清理过期数据

### 3. 前端集成

- 确保API服务正常运行
- 检查前端配置中的API地址
- 验证数据接口返回格式

## 📚 相关文档

- [SQLite默认配置说明](sqlite_default_configuration.md)
- [混合数据库存储功能](hybrid_database_storage.md)
- [API文档](../api/README.md)
- [项目主文档](../README.md)

## 🔧 故障排除

### 常见问题

1. **数据库文件不存在**
   - 检查 `data/` 目录是否存在
   - 运行一次爬虫自动创建数据库

2. **前端无法获取数据**
   - 确认API服务正在运行
   - 检查API地址配置
   - 验证数据库中是否有数据

3. **数据库连接失败**
   - 检查文件权限
   - 确认路径配置正确
   - 运行验证脚本诊断问题

### 获取帮助

如果遇到问题，请：

1. 运行验证脚本获取详细信息
2. 检查相关日志文件
3. 参考项目文档和API说明

---

**配置完成时间**: 2025-01-12
**验证状态**: ✅ 通过
**支持平台**: 全部7个平台
**存储方式**: SQLite (默认) + MySQL (可选)