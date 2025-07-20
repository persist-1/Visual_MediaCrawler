# MediaCrawler 数据库分析工具

这个工具模块用于分析 MediaCrawler 项目的 SQLite 数据库结构，并导出为 SQL 文件和 Python 数据模型文件，方便快速复现数据库结构。

## 📁 文件说明

### 核心文件
- `db_analyzer.py` - 完整的数据库分析器，支持导出多种格式
- `quick_analyze.py` - 快速分析脚本，用于查看数据库结构概览
- `run_analyzer.bat` - Windows 批处理脚本，提供交互式操作界面
- `README.md` - 本说明文档

### 输出目录
- `output/` - 分析结果输出目录（自动创建）

## 🚀 使用方法

### 方法一：使用批处理脚本（推荐）

双击运行 `run_analyzer.bat`，根据提示选择操作：

```
选择操作:
1. 快速查看数据库结构
2. 完整分析并导出文件
3. 退出
```

### 方法二：直接运行 Python 脚本

#### 快速分析
```bash
# 使用默认数据库路径
python quick_analyze.py

# 指定数据库路径
python quick_analyze.py "path/to/your/database.db"
```

#### 完整分析
```bash
python db_analyzer.py
```

## 📊 输出文件说明

完整分析会生成以下文件（带时间戳）：

### 1. SQL 结构文件 (`database_structure_YYYYMMDD_HHMMSS.sql`)
- 包含所有表的 CREATE TABLE 语句
- 包含索引信息注释
- 包含表的行数统计
- 可直接用于重建数据库结构

### 2. Python 数据模型文件 (`datamodel_YYYYMMDD_HHMMSS.py`)
- 包含 dataclass 数据类定义
- 包含 SQLAlchemy ORM 模型定义
- 自动类型映射（SQLite → Python）
- 包含索引信息注释

### 3. JSON 分析结果 (`analysis_YYYYMMDD_HHMMSS.json`)
- 完整的数据库结构分析结果
- 机器可读格式，便于进一步处理
- 包含所有表、字段、索引的详细信息

## 🔧 功能特性

### 数据库分析
- ✅ 自动发现所有数据表
- ✅ 分析表结构（字段名、类型、约束）
- ✅ 分析索引信息
- ✅ 统计表行数
- ✅ 提取原始 CREATE TABLE 语句

### 类型映射
- ✅ SQLite → Python 类型自动映射
- ✅ SQLite → SQLAlchemy 类型自动映射
- ✅ 支持可选类型（Optional）处理
- ✅ 智能命名转换（表名 → 类名）

### 输出格式
- ✅ SQL 文件（可直接执行）
- ✅ Python 数据模型（dataclass + SQLAlchemy）
- ✅ JSON 分析结果（机器可读）
- ✅ 控制台友好显示

## 📋 支持的数据表

工具会自动分析 MediaCrawler 数据库中的所有表，包括但不限于：

- `bilibili_video` - B站视频信息
- `bilibili_video_comment` - B站视频评论
- `bilibili_up_info` - B站UP主信息
- `douyin_aweme` - 抖音视频信息
- `douyin_aweme_comment` - 抖音视频评论
- `dy_creator` - 抖音创作者信息
- `kuaishou_video` - 快手视频信息
- `xhs_note` - 小红书笔记信息
- `weibo_note` - 微博内容信息
- `zhihu_content` - 知乎内容信息
- `tieba_note` - 贴吧帖子信息
- 以及其他相关表...

## 🛠️ 环境要求

- Python 3.7+
- SQLite3（Python 内置）
- 无需额外依赖

## 💡 使用场景

### 1. 数据库结构备份
导出 SQL 文件作为数据库结构的备份，便于在其他环境中重建。

### 2. 数据模型开发
生成的 Python 数据模型可直接用于：
- API 开发（FastAPI、Django 等）
- 数据分析脚本
- ETL 数据处理
- 单元测试

### 3. 数据库迁移
- 从 SQLite 迁移到 MySQL/PostgreSQL
- 数据库版本升级
- 结构对比分析

### 4. 文档生成
自动生成数据库文档，了解表结构和字段含义。

## 🔍 示例输出

### 快速分析输出
```
📊 数据库文件: ../data/mc.db
================================================================================

📋 发现 15 个数据表:
----------------------------------------
 1. bilibili_video              (   1234 行, 20 列)
 2. bilibili_video_comment      (   5678 行, 15 列)
 3. douyin_aweme               (    890 行, 25 列)
 ...
```

### 完整分析输出
```
🔍 开始分析数据库...
📊 发现 15 个数据表
📋 分析表: bilibili_video
📋 分析表: bilibili_video_comment
...
✅ 数据库分析完成，共分析 15 个表
📝 导出SQL文件到: ./output/database_structure_20241212_143022.sql
🐍 导出数据模型文件到: ./output/datamodel_20241212_143022.py
📄 导出分析结果到: ./output/analysis_20241212_143022.json

🎉 所有文件导出完成!
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个工具！

## 📄 许可证

本工具遵循 MediaCrawler 项目的许可证。