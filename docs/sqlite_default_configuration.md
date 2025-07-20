# SQLite 默认数据存储配置指南

## 概述

本项目已将 SQLite 配置为默认的数据存储方式，提供了轻量级、高性能的本地数据库解决方案。SQLite 数据库文件位于 `data/mc.db`，无需额外的数据库服务器配置。

## 配置详情

### 1. 基础配置 (base_config.py)

```python
# 数据保存类型：已设置为 'db' 模式
SAVE_DATA_OPTION = "db"  # csv or db or json

# 数据库类型：已设置为 SQLite
DB_TYPE = "sqlite"  # mysql or sqlite

# MySQL 同步功能：可选择是否同时保存到 MySQL
SYNC_TO_MYSQL = False  # 设置为 True 可启用混合存储
```

### 2. 数据库配置 (db_config.py)

```python
# SQLite 数据库文件路径
SQLITE_DB_PATH = "d:\\A_work\\A_trae_alter\\MediaCrawler-main\\data\\mc.db"

# 数据库类型常量
DB_TYPE_SQLITE = "sqlite"
```

## 功能特性

### ✅ 优势

1. **零配置启动**：无需安装和配置数据库服务器
2. **高性能**：本地文件访问，读写速度快
3. **数据完整性**：支持事务和 ACID 特性
4. **自动去重**：内置数据去重功能，避免重复爬取
5. **跨平台兼容**：支持 Windows、macOS、Linux
6. **轻量级**：数据库文件体积小，便于备份和迁移

### 📊 支持的数据类型

- **内容数据**：帖子、视频、文章等主要内容
- **评论数据**：一级评论和二级评论
- **用户数据**：创作者信息和用户资料
- **关系数据**：粉丝关注关系
- **动态数据**：用户动态和互动信息

## 数据库结构

### 支持的平台表

| 平台 | 内容表 | 评论表 | 用户表 |
|------|--------|--------|---------|
| 小红书 | `xhs_note` | `xhs_note_comment` | `xhs_creator` |
| 抖音 | `douyin_aweme` | `douyin_aweme_comment` | `dy_creator` |
| 快手 | `kuaishou_video` | `kuaishou_video_comment` | `ks_creator` |
| B站 | `bilibili_video` | `bilibili_video_comment` | `bilibili_up_info` |
| 微博 | `weibo_note` | `weibo_note_comment` | `weibo_creator` |
| 贴吧 | `tieba_note` | `tieba_note_comment` | `tieba_creator` |
| 知乎 | `zhihu_note` | `zhihu_note_comment` | `zhihu_creator` |

### 数据表特性

- **自增主键**：每个表都有自动递增的主键 `id`
- **时间戳**：`add_ts` 和 `last_modify_ts` 记录创建和修改时间
- **索引优化**：关键字段建立索引，提升查询性能
- **数据类型适配**：针对 SQLite 优化的数据类型定义

## 使用方法

### 1. 启动爬虫

```bash
# 使用默认配置启动（已配置为 SQLite）
python main.py

# 或指定平台启动
python main.py --platform xhs --keywords "编程副业"
```

### 2. 数据查看

#### 方法一：使用 API 接口

```bash
# 启动 API 服务
python api/api.py

# 访问数据接口
GET http://localhost:8000/api/notes
GET http://localhost:8000/api/comments
GET http://localhost:8000/api/creators
```

#### 方法二：直接查询数据库

```python
import sqlite3

# 连接数据库
conn = sqlite3.connect('data/mc.db')
cursor = conn.cursor()

# 查询小红书笔记
cursor.execute("SELECT * FROM xhs_note LIMIT 10")
results = cursor.fetchall()

# 关闭连接
conn.close()
```

#### 方法三：使用前端界面

```bash
# 前端服务已启动，访问：
# http://localhost:3000
```

### 3. 数据备份

```bash
# 备份整个数据库文件
cp data/mc.db data/mc_backup_$(date +%Y%m%d).db

# 或使用 SQLite 命令
sqlite3 data/mc.db ".backup data/mc_backup.db"
```

## 高级配置

### 1. 启用混合存储

如果需要同时保存到 MySQL，可以启用混合存储模式：

```python
# 在 base_config.py 中设置
SYNC_TO_MYSQL = True

# 确保 MySQL 配置正确
RELATION_DB_HOST = "localhost"
RELATION_DB_USER = "root"
RELATION_DB_PWD = "password"
RELATION_DB_NAME = "media_crawler"
```

### 2. 自定义数据库路径

```python
# 在 db_config.py 中修改
SQLITE_DB_PATH = "/custom/path/to/database.db"
```

### 3. 性能优化

```python
# 调整并发数量
MAX_CONCURRENCY_NUM = 1  # SQLite 建议使用较低的并发数

# 控制爬取数量
CRAWLER_MAX_NOTES_COUNT = 200
CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES = 10
```

## 故障排除

### 常见问题

1. **数据库文件不存在**
   - 解决方案：程序会自动创建数据库文件和目录

2. **权限问题**
   - 解决方案：确保对 `data` 目录有读写权限

3. **数据库锁定**
   - 解决方案：确保没有其他程序占用数据库文件

4. **表结构不存在**
   ```bash
   # 初始化数据库表结构
   python db.py
   ```

### 日志查看

```bash
# 查看数据库操作日志
tail -f logs/mediacrawler.log | grep -i sqlite
```

## 性能监控

### 数据库大小监控

```bash
# 查看数据库文件大小
ls -lh data/mc.db

# 查看表记录数量
sqlite3 data/mc.db "SELECT name, COUNT(*) FROM sqlite_master WHERE type='table';"
```

### 查询性能优化

```sql
-- 查看查询计划
EXPLAIN QUERY PLAN SELECT * FROM xhs_note WHERE note_id = 'xxx';

-- 分析数据库
ANALYZE;

-- 重建索引
REINDEX;
```

## 最佳实践

### 1. 数据管理

- **定期备份**：建议每日备份数据库文件
- **清理旧数据**：定期清理过期或无用数据
- **监控大小**：关注数据库文件大小增长

### 2. 性能优化

- **合理并发**：SQLite 适合低并发场景
- **批量操作**：使用事务进行批量插入
- **索引维护**：定期重建索引提升性能

### 3. 安全考虑

- **文件权限**：设置适当的文件访问权限
- **备份加密**：敏感数据备份时考虑加密
- **访问控制**：限制数据库文件的访问范围

## 技术支持

如果遇到问题，可以：

1. 查看项目文档：`README.md`
2. 检查日志文件：`logs/` 目录
3. 参考 API 文档：`api/README.md`
4. 查看测试用例：`test/` 目录

---

**注意**：SQLite 作为默认存储方案，适合中小规模的数据爬取任务。如需处理大规模数据或高并发场景，建议考虑使用 MySQL 或启用混合存储模式。