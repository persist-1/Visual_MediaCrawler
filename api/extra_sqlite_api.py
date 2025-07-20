# -*- coding: utf-8 -*-
# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：
# 1. 不得用于任何商业用途。
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。
# 3. 不得进行大规模爬取或对平台造成运营干扰。
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。
# 5. 不得用于任何非法或不当的用途。
#
# 详细许可条款请参阅项目根目录下的LICENSE文件。
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。

import asyncio
import aiosqlite
import csv
import io
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from fastapi import HTTPException
from fastapi.responses import StreamingResponse

# 获取项目根目录并添加到系统路径中以支持本地模块导入
import sys
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))
from config.db_config import SQLITE_DB_PATH


# 数据库路径
DB_PATH = SQLITE_DB_PATH

# 数据表配置
TABLE_CONFIGS = {
    'bilibili_video': {
        'name': 'B站视频',
        'primary_key': 'video_id',
        'time_field': 'create_time',
        'display_fields': ['video_id', 'title', 'desc', 'nickname', 'view_count', 'like_count', 'create_time']
    },
    'bilibili_video_comment': {
        'name': 'B站视频评论',
        'primary_key': 'comment_id',
        'time_field': 'create_time',
        'display_fields': ['comment_id', 'video_id', 'content', 'nickname', 'like_count', 'create_time']
    },
    'douyin_aweme': {
        'name': '抖音视频',
        'primary_key': 'aweme_id',
        'time_field': 'create_time',
        'display_fields': ['aweme_id', 'desc', 'nickname', 'digg_count', 'comment_count', 'create_time']
    },
    'douyin_aweme_comment': {
        'name': '抖音视频评论',
        'primary_key': 'comment_id',
        'time_field': 'create_time',
        'display_fields': ['comment_id', 'aweme_id', 'content', 'nickname', 'digg_count', 'create_time']
    },
    'kuaishou_video': {
        'name': '快手视频',
        'primary_key': 'video_id',
        'time_field': 'create_time',
        'display_fields': ['video_id', 'title', 'desc', 'nickname', 'view_count', 'like_count', 'create_time']
    },
    'kuaishou_video_comment': {
        'name': '快手视频评论',
        'primary_key': 'comment_id',
        'time_field': 'create_time',
        'display_fields': ['comment_id', 'video_id', 'content', 'nickname', 'like_count', 'create_time']
    },
    'xhs_note': {
        'name': '小红书笔记',
        'primary_key': 'note_id',
        'time_field': 'time',
        'display_fields': ['note_id', 'title', 'desc', 'nickname', 'liked_count', 'collected_count', 'time']
    },
    'xhs_note_comment': {
        'name': '小红书笔记评论',
        'primary_key': 'comment_id',
        'time_field': 'create_time',
        'display_fields': ['comment_id', 'note_id', 'content', 'nickname', 'like_count', 'create_time']
    },
    'weibo_note': {
        'name': '微博内容',
        'primary_key': 'note_id',
        'time_field': 'create_time',
        'display_fields': ['note_id', 'title', 'desc', 'nickname', 'attitudes_count', 'comments_count', 'create_time']
    },
    'weibo_note_comment': {
        'name': '微博评论',
        'primary_key': 'comment_id',
        'time_field': 'create_time',
        'display_fields': ['comment_id', 'note_id', 'content', 'nickname', 'like_count', 'create_time']
    },
    'tieba_note': {
        'name': '贴吧帖子',
        'primary_key': 'note_id',
        'time_field': 'publish_time',
        'display_fields': ['note_id', 'title', 'desc', 'user_nickname', 'tieba_name', 'total_replay_num', 'publish_time']
    },
    'tieba_comment': {
        'name': '贴吧评论',
        'primary_key': 'comment_id',
        'time_field': 'publish_time',
        'display_fields': ['comment_id', 'note_id', 'content', 'user_nickname', 'publish_time']
    },
    'zhihu_content': {
        'name': '知乎内容',
        'primary_key': 'content_id',
        'time_field': 'created_time',
        'display_fields': ['content_id', 'title', 'desc', 'user_nickname', 'voteup_count', 'comment_count', 'created_time']
    },
    'zhihu_comment': {
        'name': '知乎评论',
        'primary_key': 'comment_id',
        'time_field': 'publish_time',
        'display_fields': ['comment_id', 'content_id', 'content', 'user_nickname', 'like_count', 'publish_time']
    },
    'crawler_tasks': {
        'name': '爬虫任务',
        'primary_key': 'task_times_id',
        'time_field': 'created_at',
        'display_fields': ['task_times_id', 'status', 'platform', 'crawler_type', 'keywords', 'created_at', 'updated_at']
    }
}

class SQLiteDataManager:
    """SQLite数据管理器"""
    
    def __init__(self, db_path: str = None):
        # 使用配置文件中的路径，确保路径格式正确
        if db_path:
            self.db_path = str(Path(db_path).resolve())
        else:
            # 确保从配置文件获取的路径格式正确
            self.db_path = str(Path(DB_PATH).resolve())
    
    def get_connection(self):
        """获取数据库连接"""
        try:
            return aiosqlite.connect(self.db_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"数据库连接失败: {str(e)}")
    
    async def get_available_tables(self) -> List[str]:
        """获取可用的数据表列表"""
        async with self.get_connection() as db:
            cursor = await db.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )
            tables = await cursor.fetchall()
            return [table[0] for table in tables if table[0] in TABLE_CONFIGS]
    
    async def get_table_data(self, table_name: str, page: int = 1, page_size: int = 30, task_times_id: str = None) -> Dict[str, Any]:
        """获取表格数据"""
        if table_name not in TABLE_CONFIGS:
            raise HTTPException(status_code=400, detail=f"不支持的数据表: {table_name}")
        
        offset = (page - 1) * page_size
        
        async with self.get_connection() as db:
            # 构建WHERE条件
            where_conditions = []
            params = []
            
            # 如果指定了任务ID，添加筛选条件
            if task_times_id:
                # 对于爬虫任务表，使用task_times_id字段
                if table_name == 'crawler_tasks':
                    where_conditions.append("task_times_id = ?")
                else:
                    # 对于数据表，使用task_times_id字段
                    where_conditions.append("task_times_id = ?")
                params.append(task_times_id)
            
            where_clause = f"WHERE {' AND '.join(where_conditions)}" if where_conditions else ""
            
            # 获取总数
            count_query = f"SELECT COUNT(*) FROM {table_name} {where_clause}"
            count_cursor = await db.execute(count_query, params)
            total_result = await count_cursor.fetchone()
            total = total_result[0] if total_result else 0
            
            # 获取数据
            config = TABLE_CONFIGS[table_name]
            time_field = config.get('time_field', 'create_time')
            
            # 构建查询语句，按时间倒序排列
            query = f"""
                SELECT * FROM {table_name} 
                {where_clause}
                ORDER BY {time_field} DESC 
                LIMIT {page_size} OFFSET {offset}
            """
            
            # 为分页查询添加参数
            data_params = params.copy()
            data_cursor = await db.execute(query, data_params)
            columns = [description[0] for description in data_cursor.description]
            rows = await data_cursor.fetchall()
            
            # 转换为字典列表
            data = []
            for row in rows:
                row_dict = {}
                for i, value in enumerate(row):
                    row_dict[columns[i]] = value
                data.append(row_dict)
            
            return {
                'data': data,
                'total': total,
                'page': page,
                'page_size': page_size,
                'total_pages': (total + page_size - 1) // page_size,
                'task_times_id': task_times_id  # 返回当前筛选的任务ID
            }
    
    async def get_data_statistics(self) -> Dict[str, Any]:
        """获取数据统计信息"""
        stats = {
            'total': 0,
            'tables': 0,
            'today': 0,
            'lastUpdate': None
        }
        
        try:
            async with self.get_connection() as db:
                # 获取表数量
                tables = await self.get_available_tables()
                stats['tables'] = len(tables)
                
                # 计算总数据量和今日新增
                today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                today_timestamp = int(today.timestamp())
                
                total_count = 0
                today_count = 0
                latest_time = None
                
                for table in tables:
                    config = TABLE_CONFIGS.get(table, {})
                    time_field = config.get('time_field', 'create_time')
                    
                    # 总数量
                    count_cursor = await db.execute(f"SELECT COUNT(*) FROM {table}")
                    count_result = await count_cursor.fetchone()
                    if count_result:
                        total_count += count_result[0]
                    
                    # 今日新增
                    today_cursor = await db.execute(
                        f"SELECT COUNT(*) FROM {table} WHERE {time_field} >= ?",
                        (today_timestamp,)
                    )
                    today_result = await today_cursor.fetchone()
                    if today_result:
                        today_count += today_result[0]
                    
                    # 最新更新时间
                    time_cursor = await db.execute(
                        f"SELECT MAX({time_field}) FROM {table}"
                    )
                    time_result = await time_cursor.fetchone()
                    if time_result and time_result[0]:
                        table_latest = time_result[0]
                        if latest_time is None or table_latest > latest_time:
                            latest_time = table_latest
                
                stats['total'] = total_count
                stats['today'] = today_count
                if latest_time:
                    stats['lastUpdate'] = datetime.fromtimestamp(latest_time).isoformat()
                
        except Exception as e:
            print(f"获取数据统计失败: {e}")
        
        return stats
    
    # 任务管理方法
    async def create_task(self, task_times_id: str, task_data: Dict[str, Any]) -> str:
        """创建新任务"""
        now = datetime.now().isoformat()
        
        async with self.get_connection() as db:
            query = """
            INSERT INTO crawler_tasks (
                task_times_id, status, message, result_stdout, result_stderr,
                created_at, updated_at, platform, crawler_type, keywords,
                login_type, start_page, max_count, get_comment, get_sub_comment,
                sync_to_mysql, specified_ids, creator_ids, cookies, save_format
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            values = (
                task_times_id,
                task_data.get('status', 'pending'),
                task_data.get('message'),
                task_data.get('result_stdout'),
                task_data.get('result_stderr'),
                now,
                now,
                task_data.get('platform'),
                task_data.get('crawler_type'),
                task_data.get('keywords'),
                task_data.get('login_type'),
                task_data.get('start_page'),
                task_data.get('max_count'),
                task_data.get('get_comment'),
                task_data.get('get_sub_comment'),
                1 if task_data.get('sync_to_mysql') else 0,
                task_data.get('specified_ids'),
                task_data.get('creator_ids'),
                task_data.get('cookies'),
                task_data.get('save_format', 'csv')
            )
            
            await db.execute(query, values)
            await db.commit()
            return task_times_id
    
    async def get_task(self, task_times_id: str) -> Optional[Dict[str, Any]]:
        """获取单个任务"""
        async with self.get_connection() as db:
            cursor = await db.execute("SELECT * FROM crawler_tasks WHERE task_times_id = ?", (task_times_id,))
            row = await cursor.fetchone()
            
            if not row:
                return None
            
            # 获取列名
            columns = [desc[0] for desc in cursor.description]
            task = dict(zip(columns, row))
            
            # 重构result字段
            task['result'] = {
                'stdout': task.pop('result_stdout', ''),
                'stderr': task.pop('result_stderr', '')
            }
            
            return task
    
    async def update_task_status(self, task_times_id: str, status: str, message: str = None, 
                                result_stdout: str = None, result_stderr: str = None) -> bool:
        """更新任务状态"""
        now = datetime.now().isoformat()
        
        # 构建更新字段
        update_fields = ['status = ?', 'updated_at = ?']
        values = [status, now]
        
        if message is not None:
            update_fields.append('message = ?')
            values.append(message)
        
        if result_stdout is not None:
            update_fields.append('result_stdout = ?')
            values.append(result_stdout)
        
        if result_stderr is not None:
            update_fields.append('result_stderr = ?')
            values.append(result_stderr)
        
        values.append(task_times_id)
        
        query = f"UPDATE crawler_tasks SET {', '.join(update_fields)} WHERE task_times_id = ?"
        
        try:
            async with self.get_connection() as db:
                await db.execute(query, values)
                await db.commit()
                return True
        except Exception as e:
            print(f"更新任务状态失败: {e}")
            return False
    
    async def get_all_tasks(self) -> Dict[str, Any]:
        """获取所有任务（兼容原JSON格式）"""
        async with self.get_connection() as db:
            cursor = await db.execute("SELECT * FROM crawler_tasks ORDER BY created_at DESC")
            rows = await cursor.fetchall()
            
            if not rows:
                return {}
            
            # 获取列名
            columns = [desc[0] for desc in cursor.description]
            
            tasks = {}
            for row in rows:
                task_data = dict(zip(columns, row))
                task_times_id = task_data.pop('task_times_id')
                task_data.pop('id', None)  # 移除数据库ID
                
                # 重构result字段
                task_data['result'] = {
                    'stdout': task_data.pop('result_stdout', ''),
                    'stderr': task_data.pop('result_stderr', '')
                }
                
                # 转换布尔值
                for bool_field in ['get_comment', 'get_sub_comment', 'sync_to_mysql']:
                    if task_data.get(bool_field) is not None:
                        task_data[bool_field] = bool(task_data[bool_field])
                
                tasks[task_times_id] = task_data
            
            return tasks
    
    async def delete_task(self, task_times_id: str) -> bool:
        """删除任务"""
        try:
            async with self.get_connection() as db:
                await db.execute("DELETE FROM crawler_tasks WHERE task_times_id = ?", (task_times_id,))
                await db.commit()
                return True
        except Exception as e:
            print(f"删除任务失败: {e}")
            return False
    
    async def export_table_data(self, table_name: str, task_id: str = None) -> StreamingResponse:
        """导出表格数据为CSV"""
        if table_name not in TABLE_CONFIGS:
            raise HTTPException(status_code=400, detail=f"不支持的数据表: {table_name}")
        
        async with self.get_connection() as db:
            # 构建WHERE条件
            where_conditions = []
            params = []
            
            # 如果指定了任务ID，添加筛选条件
            if task_id:
                if table_name == 'crawler_tasks':
                    where_conditions.append("task_times_id = ?")
                else:
                    where_conditions.append("task_times_id = ?")
                params.append(task_id)
            
            where_clause = f"WHERE {' AND '.join(where_conditions)}" if where_conditions else ""
            
            # 获取数据
            config = TABLE_CONFIGS[table_name]
            time_field = config.get('time_field', 'create_time')
            
            query = f"SELECT * FROM {table_name} {where_clause} ORDER BY {time_field} DESC"
            
            cursor = await db.execute(query, params)
            columns = [description[0] for description in cursor.description]
            rows = await cursor.fetchall()
            
            # 创建CSV内容
            output = io.StringIO()
            writer = csv.writer(output)
            
            # 写入表头
            writer.writerow(columns)
            
            # 写入数据
            for row in rows:
                writer.writerow(row)
            
            # 准备响应
            output.seek(0)
            csv_content = output.getvalue()
            output.close()
            
            # 创建文件名
            filename = f"{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            # 返回流式响应
            return StreamingResponse(
                io.StringIO(csv_content),
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

# 创建全局实例
sqlite_manager = SQLiteDataManager()

# API路由函数
async def get_sqlite_tables():
    """获取可用的SQLite数据表列表"""
    try:
        tables = await sqlite_manager.get_available_tables()
        return {
            "success": True,
            "message": "获取数据表列表成功",
            "data": tables
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取数据表列表失败: {str(e)}")

async def get_sqlite_data(table: str, page: int = 1, page_size: int = 30, task_times_id: str = None):
    """获取SQLite表格数据"""
    try:
        if page < 1:
            page = 1
        if page_size < 1 or page_size > 1000:
            page_size = 30
            
        data = await sqlite_manager.get_table_data(table, page, page_size, task_times_id)
        return {
            "success": True,
            "message": "获取数据成功",
            "data": data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取数据失败: {str(e)}")

async def get_sqlite_stats():
    """获取SQLite数据统计"""
    try:
        stats = await sqlite_manager.get_data_statistics()
        return {
            "success": True,
            "message": "获取统计数据成功",
            "data": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计数据失败: {str(e)}")

async def export_sqlite_data(table_name: str, task_id: str = None):
    """导出SQLite表格数据"""
    try:
        return await sqlite_manager.export_table_data(table_name, task_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出数据失败: {str(e)}")

async def export_sqlite_data_as_json(table_name: str, task_id: str = None):
    """导出SQLite表格数据为JSON格式"""
    try:
        if table_name not in TABLE_CONFIGS:
            raise HTTPException(status_code=400, detail=f"不支持的数据表: {table_name}")
        
        async with sqlite_manager.get_connection() as db:
            # 构建WHERE条件
            where_conditions = []
            params = []
            
            # 如果指定了任务ID，添加筛选条件
            if task_id:
                if table_name == 'crawler_tasks':
                    where_conditions.append("task_times_id = ?")
                else:
                    where_conditions.append("task_times_id = ?")
                params.append(task_id)
            
            where_clause = f"WHERE {' AND '.join(where_conditions)}" if where_conditions else ""
            
            # 获取数据
            config = TABLE_CONFIGS[table_name]
            time_field = config.get('time_field', 'create_time')
            
            query = f"SELECT * FROM {table_name} {where_clause} ORDER BY {time_field} DESC"
            
            cursor = await db.execute(query, params)
            columns = [description[0] for description in cursor.description]
            rows = await cursor.fetchall()
            
            # 转换为字典列表
            data = []
            for row in rows:
                row_dict = {}
                for i, value in enumerate(row):
                    row_dict[columns[i]] = value
                data.append(row_dict)
            
            return {
                "success": True,
                "message": "导出JSON数据成功",
                "data": {
                    "table_name": table_name,
                    "total_count": len(data),
                    "task_id_filter": task_id,
                    "export_time": datetime.now().isoformat(),
                    "records": data
                }
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出JSON数据失败: {str(e)}")

# 表格配置信息
def get_table_configs():
    """获取表格配置信息"""
    return {
        "success": True,
        "message": "获取表格配置成功",
        "data": TABLE_CONFIGS
    }

# 任务管理API函数
async def create_task(task_times_id: str, task_data: Dict[str, Any]) -> str:
    """创建新任务"""
    return await sqlite_manager.create_task(task_times_id, task_data)

async def get_task(task_times_id: str) -> Optional[Dict[str, Any]]:
    """获取单个任务"""
    return await sqlite_manager.get_task(task_times_id)

async def update_task_status(task_times_id: str, status: str, message: str = None, result: Dict[str, Any] = None) -> bool:
    """更新任务状态"""
    result_stdout = None
    result_stderr = None
    
    if result:
        result_stdout = result.get('stdout')
        result_stderr = result.get('stderr')
    
    return await sqlite_manager.update_task_status(task_times_id, status, message, result_stdout, result_stderr)

async def get_all_tasks() -> Dict[str, Any]:
    """获取所有任务"""
    return await sqlite_manager.get_all_tasks()

async def delete_task(task_times_id: str) -> bool:
    """删除任务"""
    return await sqlite_manager.delete_task(task_times_id)