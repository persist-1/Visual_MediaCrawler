# 混合数据库存储功能使用说明

## 功能概述

本项目新增了混合数据库存储功能，支持同时将爬取的数据保存到 SQLite 和 MySQL 数据库中。这个功能为用户提供了更灵活的数据存储选择：

- **SQLite**：作为本地数据库，提供快速的本地数据访问和备份
- **MySQL**：作为远程数据库，支持多用户访问和更强的数据管理能力

## 配置说明

### 1. 启用混合存储模式

在 `config/base_config.py` 中设置以下配置：

```python
# 数据保存类型选择数据库模式
SAVE_DATA_OPTION = "db"

# 是否同步保存至MySQL数据库
SYNC_TO_MYSQL = True
```

### 2. 数据库配置

#### SQLite 配置
SQLite 数据库会自动创建在项目目录下，无需额外配置。

#### MySQL 配置
在 `config/db_config.py` 中配置 MySQL 连接信息：

```python
# MySQL数据库配置
MYSQL_DB_HOST = "localhost"
MYSQL_DB_PORT = 3306
MYSQL_DB_USER = "your_username"
MYSQL_DB_PWD = "your_password"
MYSQL_DB_NAME = "media_crawler"
```

## 支持的平台

混合数据库存储功能支持以下所有平台：

- ✅ 小红书 (XHS)
- ✅ 抖音 (Douyin)
- ✅ 快手 (Kuaishou)
- ✅ 微博 (Weibo)
- ✅ 贴吧 (Tieba)
- ✅ 知乎 (Zhihu)
- ✅ B站 (Bilibili)

## 工作原理

### 数据流程

1. **数据采集**：爬虫采集到数据后，首先保存到 SQLite 数据库
2. **MySQL 同步**：如果启用了 `SYNC_TO_MYSQL`，数据会同时保存到 MySQL 数据库
3. **错误处理**：如果 MySQL 保存失败，不会影响 SQLite 的保存，确保数据不丢失

### 存储策略

- **SQLite 优先**：始终优先保存到 SQLite，确保本地数据完整性
- **MySQL 可选**：MySQL 作为可选的远程存储，通过配置控制是否启用
- **异步处理**：两个数据库的保存操作都是异步进行，不会阻塞爬取流程

## 使用场景

### 1. 本地开发 + 远程备份
```python
SAVE_DATA_OPTION = "db"
SYNC_TO_MYSQL = True
```
适用于：个人开发者希望在本地快速访问数据，同时备份到远程 MySQL 服务器。

### 2. 仅本地存储
```python
SAVE_DATA_OPTION = "db"
SYNC_TO_MYSQL = False
```
适用于：只需要本地数据存储，不需要远程数据库的场景。

### 3. 团队协作
```python
SAVE_DATA_OPTION = "db"
SYNC_TO_MYSQL = True
# 配置共享的MySQL服务器
```
适用于：团队成员需要共享爬取的数据，通过 MySQL 实现数据共享。

## 数据表结构

混合存储模式使用相同的数据表结构，确保 SQLite 和 MySQL 中的数据完全一致。主要数据表包括：

### 内容表
- `xhs_note` - 小红书笔记
- `douyin_aweme` - 抖音视频
- `kuaishou_video` - 快手视频
- `weibo_note` - 微博内容
- `tieba_note` - 贴吧帖子
- `zhihu_note` - 知乎内容
- `bilibili_video` - B站视频

### 评论表
- `xhs_note_comment` - 小红书评论
- `douyin_aweme_comment` - 抖音评论
- `kuaishou_video_comment` - 快手评论
- `weibo_note_comment` - 微博评论
- `tieba_note_comment` - 贴吧评论
- `zhihu_note_comment` - 知乎评论
- `bilibili_video_comment` - B站评论

### 创作者表
- `xhs_creator` - 小红书创作者
- `douyin_aweme_creator` - 抖音创作者
- `kuaishou_creator` - 快手创作者
- `weibo_creator` - 微博创作者
- `tieba_creator` - 贴吧创作者
- `zhihu_creator` - 知乎创作者
- `bilibili_creator` - B站创作者

## 性能考虑

### 优势
- **数据安全**：双重备份，降低数据丢失风险
- **访问灵活**：本地快速访问 + 远程共享访问
- **扩展性强**：支持后续添加更多数据库类型

### 注意事项
- **存储空间**：会占用更多存储空间（SQLite + MySQL）
- **网络依赖**：MySQL 同步需要稳定的网络连接
- **性能影响**：同时写入两个数据库会略微增加处理时间

## 故障排除

### 1. MySQL 连接失败
```
错误：MySQL连接失败
解决：检查 MySQL 服务是否启动，配置信息是否正确
```

### 2. 数据同步失败
```
错误：MySQL 数据保存失败
影响：不影响 SQLite 数据保存
解决：检查 MySQL 服务状态和网络连接
```

### 3. 表结构不匹配
```
错误：表结构不存在或不匹配
解决：运行数据库初始化脚本创建表结构
```

## 最佳实践

1. **开发阶段**：使用 SQLite 进行快速开发和测试
2. **生产环境**：启用 MySQL 同步，确保数据备份和共享
3. **定期备份**：定期备份 SQLite 文件和 MySQL 数据
4. **监控日志**：关注日志中的数据库操作信息，及时发现问题

## 技术实现

### 核心类
每个平台都实现了对应的混合存储类：
- `XhsHybridDbStoreImplement`
- `DouyinHybridDbStoreImplement`
- `KuaishouHybridDbStoreImplement`
- `WeiboHybridDbStoreImplement`
- `TieBaHybridDbStoreImplement`
- `ZhihuHybridDbStoreImplement`
- `BilibiliHybridDbStoreImplement`

### 关键方法
```python
async def store_content(self, content_item: Dict):
    """同时保存内容到 SQLite 和 MySQL"""
    # 保存到 SQLite
    await self.sqlite_store.store_content(content_item)
    
    # 如果启用 MySQL 同步，则保存到 MySQL
    if config.SYNC_TO_MYSQL:
        mysql_store = await self._get_mysql_store()
        if mysql_store:
            await mysql_store.store_content(content_item)
```

## 更新日志

### v1.0.0 (2024-01-XX)
- ✅ 新增混合数据库存储功能
- ✅ 支持所有平台的数据同步
- ✅ 添加配置选项控制 MySQL 同步
- ✅ 完善错误处理和日志记录

---

如有问题或建议，请提交 Issue 或 Pull Request。