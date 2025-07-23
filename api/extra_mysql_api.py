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
import csv
import io
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

import aiomysql
from fastapi import HTTPException
from fastapi.responses import StreamingResponse

# 导入配置和数据库操作模块
sys_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if sys_path not in os.sys.path:
    os.sys.path.append(sys_path)

from config.db_config import (
    MYSQL_DB_HOST, MYSQL_DB_PORT, MYSQL_DB_USER, MYSQL_DB_PWD, MYSQL_DB_NAME,
    AsyncMysqlDB
)
from dp_op.db_tables_mapping import (
    get_all_detailed_table_configs,
    get_detailed_table_config,
    is_valid_table,
    get_table_display_name
)

class MySQLDataManager:
    """MySQL数据管理器"""
    
    def __init__(self):
        self.pool: Optional[aiomysql.Pool] = None
        self.db: Optional[AsyncMysqlDB] = None
        
        # 从统一配置模块获取表格配置信息
        self.table_configs = get_all_detailed_table_configs()
    
    async def get_connection(self) -> AsyncMysqlDB:
        """获取数据库连接"""
        if self.pool is None:
            try:
                self.pool = await aiomysql.create_pool(
                    host=MYSQL_DB_HOST,
                    port=int(MYSQL_DB_PORT),
                    user=MYSQL_DB_USER,
                    password=MYSQL_DB_PWD,
                    db=MYSQL_DB_NAME,
                    charset='utf8mb4',
                    autocommit=True,
                    maxsize=10,
                    minsize=1
                )
                self.db = AsyncMysqlDB(self.pool)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"MySQL数据库连接失败: {str(e)}")
        
        return self.db
    
    async def close_connection(self):
        """关闭数据库连接"""
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            self.pool = None
            self.db = None
    
    async def get_available_tables(self) -> List[Dict[str, Any]]:
        """获取可用的数据表列表"""
        db = await self.get_connection()
        
        try:
            # 查询数据库中的所有表
            tables_query = "SHOW TABLES"
            tables_result = await db.query(tables_query)
            
            available_tables = []
            for table_row in tables_result:
                table_name = list(table_row.values())[0]
                
                # 获取表的记录数
                count_query = f"SELECT COUNT(*) as count FROM `{table_name}`"
                count_result = await db.get_first(count_query)
                record_count = count_result['count'] if count_result else 0
                
                # 获取表配置信息
                table_config = self.table_configs.get(table_name, {
                    "name": table_name,
                    "description": f"{table_name}数据表",
                    "columns": []
                })
                
                available_tables.append({
                    "table_name": table_name,
                    "display_name": table_config["name"],
                    "description": table_config["description"],
                    "record_count": record_count
                })
            
            return available_tables
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取表列表失败: {str(e)}")
    
    async def get_table_data(self, table_name: str, page: int = 1, page_size: int = 30, 
                           task_times_id: Optional[str] = None) -> Dict[str, Any]:
        """获取表格数据"""
        db = await self.get_connection()
        
        try:
            # 构建基础查询
            base_query = f"SELECT * FROM `{table_name}`"
            count_query = f"SELECT COUNT(*) as total FROM `{table_name}`"
            
            # 添加任务ID筛选条件
            where_clause = ""
            query_params = []
            
            if task_times_id:
                where_clause = " WHERE task_times_id = %s"
                query_params = [task_times_id]
            
            # 获取总数
            total_result = await db.get_first(count_query + where_clause, *query_params)
            total = total_result['total'] if total_result else 0
            
            # 计算分页
            offset = (page - 1) * page_size
            
            # 构建分页查询
            data_query = base_query + where_clause + f" ORDER BY id DESC LIMIT %s OFFSET %s"
            data_params = query_params + [page_size, offset]
            
            # 获取数据
            data = await db.query(data_query, *data_params)
            
            # 处理数据格式
            processed_data = []
            for row in data:
                processed_row = {}
                for key, value in row.items():
                    if isinstance(value, datetime):
                        processed_row[key] = value.isoformat()
                    else:
                        processed_row[key] = value
                processed_data.append(processed_row)
            
            return {
                "data": processed_data,
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": (total + page_size - 1) // page_size
            }
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取表格数据失败: {str(e)}")
    
    async def get_data_statistics(self) -> Dict[str, Any]:
        """获取数据统计信息"""
        db = await self.get_connection()
        
        try:
            # 获取所有表
            tables = await self.get_available_tables()
            
            total_records = 0
            table_stats = []
            
            for table in tables:
                table_name = table["table_name"]
                record_count = table["record_count"]
                total_records += record_count
                
                # 获取今日新增数据（如果有add_ts字段）
                today_count = 0
                try:
                    today_query = f"""
                        SELECT COUNT(*) as count FROM `{table_name}` 
                        WHERE DATE(FROM_UNIXTIME(add_ts)) = CURDATE()
                    """
                    today_result = await db.get_first(today_query)
                    today_count = today_result['count'] if today_result else 0
                except:
                    # 如果表没有add_ts字段，忽略错误
                    pass
                
                # 获取最新更新时间
                latest_time = None
                try:
                    latest_query = f"""
                        SELECT FROM_UNIXTIME(MAX(add_ts)) as latest_time FROM `{table_name}`
                        WHERE add_ts IS NOT NULL
                    """
                    latest_result = await db.get_first(latest_query)
                    if latest_result and latest_result['latest_time']:
                        latest_time = latest_result['latest_time'].isoformat()
                except:
                    # 如果表没有add_ts字段，忽略错误
                    pass
                
                table_stats.append({
                    "table_name": table_name,
                    "display_name": table["display_name"],
                    "record_count": record_count,
                    "today_count": today_count,
                    "latest_update": latest_time
                })
            
            return {
                "total_records": total_records,
                "table_count": len(tables),
                "tables": table_stats
            }
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")
    
    async def create_task(self, task_times_id: str, task_data: Dict[str, Any]):
        """创建任务记录"""
        db = await self.get_connection()
        
        try:
            # 检查任务是否已存在
            existing_task = await db.get_first(
                "SELECT id FROM crawler_tasks WHERE task_times_id = %s",
                task_times_id
            )
            
            if existing_task:
                # 更新现有任务
                await db.update_table(
                    "crawler_tasks",
                    {
                        "status": task_data.get("status", "pending"),
                        "message": task_data.get("message", ""),
                        "result_stdout": task_data.get("result_stdout"),
                    "result_stderr": task_data.get("result_stderr"),
                        "platform": task_data.get("platform"),
                        "crawler_type": task_data.get("crawler_type"),
                        "keywords": task_data.get("keywords"),
                        "login_type": task_data.get("login_type"),
                        "start_page": task_data.get("start_page"),
                        "get_comment": task_data.get("get_comment"),
                        "get_sub_comment": task_data.get("get_sub_comment"),
                        "storage_type": task_data.get("storage_type", "sqlite"),
                        "updated_at": datetime.now()
                    },
                    "task_times_id",
                    task_times_id
                )
            else:
                # 创建新任务
                await db.item_to_table("crawler_tasks", {
                    "task_times_id": task_times_id,
                    "status": task_data.get("status", "pending"),
                    "message": task_data.get("message", ""),
                    "result_stdout": task_data.get("result_stdout"),
                    "result_stderr": task_data.get("result_stderr"),
                    "platform": task_data.get("platform"),
                    "crawler_type": task_data.get("crawler_type"),
                    "keywords": task_data.get("keywords"),
                    "login_type": task_data.get("login_type"),
                    "start_page": task_data.get("start_page"),
                    "get_comment": task_data.get("get_comment"),
                    "get_sub_comment": task_data.get("get_sub_comment"),
                    "storage_type": task_data.get("storage_type", "sqlite"),
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                })
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"创建任务失败: {str(e)}")
    
    async def get_task(self, task_times_id: str) -> Optional[Dict[str, Any]]:
        """获取任务信息"""
        db = await self.get_connection()
        
        try:
            task = await db.get_first(
                "SELECT * FROM crawler_tasks WHERE task_times_id = %s",
                task_times_id
            )
            
            if task:
                # 处理结果字段
                if task.get('result_stdout') or task.get('result_stderr'):
                    task['result'] = {
                        'stdout': task.get('result_stdout'),
                        'stderr': task.get('result_stderr')
                    }
                
                # 处理时间字段
                for time_field in ['created_at', 'updated_at']:
                    if task.get(time_field) and isinstance(task[time_field], datetime):
                        task[time_field] = task[time_field].isoformat()
            
            return task
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取任务失败: {str(e)}")
    
    async def update_task_status(self, task_times_id: str, status: str, message: str, result: Optional[Dict] = None):
        """更新任务状态"""
        db = await self.get_connection()
        
        try:
            update_data = {
                "status": status,
                "message": message,
                "updated_at": datetime.now()
            }
            
            if result is not None:
                update_data["result_stdout"] = result.get("stdout") if isinstance(result, dict) else None
                update_data["result_stderr"] = result.get("stderr") if isinstance(result, dict) else None
            
            await db.update_table(
                "crawler_tasks",
                update_data,
                "task_times_id",
                task_times_id
            )
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"更新任务状态失败: {str(e)}")
    
    async def get_all_tasks(self) -> Dict[str, Dict[str, Any]]:
        """获取所有任务"""
        db = await self.get_connection()
        
        try:
            tasks = await db.query(
                "SELECT * FROM crawler_tasks ORDER BY created_at DESC"
            )
            
            result = {}
            for task in tasks:
                # 处理结果字段
                if task.get('result_stdout') or task.get('result_stderr'):
                    task['result'] = {
                        'stdout': task.get('result_stdout'),
                        'stderr': task.get('result_stderr')
                    }
                
                # 处理时间字段
                for time_field in ['created_at', 'updated_at']:
                    if task.get(time_field) and isinstance(task[time_field], datetime):
                        task[time_field] = task[time_field].isoformat()
                
                result[task['task_times_id']] = task
            
            return result
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取任务列表失败: {str(e)}")
    
    async def delete_task(self, task_times_id: str):
        """删除任务及其关联的所有数据"""
        db = await self.get_connection()
        
        try:
            # 定义所有包含task_times_id字段的表
            tables_with_task_id = [
                'bilibili_video',
                'bilibili_video_comment', 
                'bilibili_up_info',
                'bilibili_contact_info',
                'bilibili_up_dynamic',
                'douyin_aweme',
                'douyin_aweme_comment',
                'dy_creator',
                'kuaishou_video',
                'kuaishou_video_comment',
                'weibo_note',
                'weibo_note_comment',
                'weibo_creator',
                'xhs_note',
                'xhs_note_comment',
                'xhs_creator',
                'tieba_note',
                'tieba_comment',
                'tieba_creator',
                'zhihu_content',
                'zhihu_comment',
                'zhihu_creator'
            ]
            
            # 删除所有关联数据表中的记录
            for table in tables_with_task_id:
                try:
                    # 检查表是否存在
                    table_check_result = await db.query(
                        "SELECT COUNT(*) as count FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = %s",
                        table
                    )
                    
                    if table_check_result and table_check_result[0]['count'] > 0:
                        # 检查表是否有task_times_id字段
                        column_check_result = await db.query(
                            "SELECT COUNT(*) as count FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = %s AND column_name = 'task_times_id'",
                            table
                        )
                        
                        if column_check_result and column_check_result[0]['count'] > 0:
                            await db.execute(
                                f"DELETE FROM `{table}` WHERE task_times_id = %s",
                                task_times_id
                            )
                            print(f"已删除表 {table} 中task_times_id为 {task_times_id} 的记录")
                except Exception as table_error:
                    print(f"删除表 {table} 中的数据时出错: {table_error}")
                    # 继续删除其他表，不因单个表的错误而中断
                    continue
            
            # 最后删除任务记录
            await db.execute(
                "DELETE FROM crawler_tasks WHERE task_times_id = %s",
                task_times_id
            )
            print(f"成功删除任务 {task_times_id} 及其所有关联数据")
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"删除任务失败: {str(e)}")
    
    async def export_table_data(self, table_name: str, task_id: Optional[str] = None) -> StreamingResponse:
        """导出表格数据为CSV"""
        db = await self.get_connection()
        
        try:
            # 构建查询
            query = f"SELECT * FROM `{table_name}`"
            params = []
            
            if task_id:
                query += " WHERE task_times_id = %s"
                params.append(task_id)
            
            query += " ORDER BY id DESC"
            
            # 获取数据
            data = await db.query(query, *params)
            
            if not data:
                raise HTTPException(status_code=404, detail="没有找到数据")
            
            # 创建CSV内容
            output = io.StringIO()
            
            # 写入BOM以支持Excel正确显示中文
            output.write('\ufeff')
            
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            
            for row in data:
                # 处理特殊字段
                processed_row = {}
                for key, value in row.items():
                    if isinstance(value, datetime):
                        processed_row[key] = value.isoformat()
                    elif value is None:
                        processed_row[key] = ''
                    else:
                        processed_row[key] = str(value)
                writer.writerow(processed_row)
            
            # 准备响应
            output.seek(0)
            content = output.getvalue()
            output.close()
            
            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{table_name}_{timestamp}.csv"
            if task_id:
                filename = f"{table_name}_{task_id}_{timestamp}.csv"
            
            return StreamingResponse(
                io.BytesIO(content.encode('utf-8')),
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"导出数据失败: {str(e)}")
    
    async def export_table_data_as_json(self, table_name: str, task_id: Optional[str] = None) -> Dict[str, Any]:
        """导出表格数据为JSON"""
        db = await self.get_connection()
        
        try:
            # 构建查询
            query = f"SELECT * FROM `{table_name}`"
            params = []
            
            if task_id:
                query += " WHERE task_times_id = %s"
                params.append(task_id)
            
            query += " ORDER BY id DESC"
            
            # 获取数据
            data = await db.query(query, *params)
            
            # 处理数据格式
            processed_data = []
            for row in data:
                processed_row = {}
                for key, value in row.items():
                    if isinstance(value, datetime):
                        processed_row[key] = value.isoformat()
                    else:
                        processed_row[key] = value
                processed_data.append(processed_row)
            
            return {
                "table_name": table_name,
                "task_id": task_id,
                "export_time": datetime.now().isoformat(),
                "total_count": len(processed_data),
                "data": processed_data
            }
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"导出JSON数据失败: {str(e)}")

# 创建全局数据管理器实例
mysql_data_manager = MySQLDataManager()

# API函数
async def get_mysql_tables():
    """获取MySQL数据表列表"""
    try:
        tables_info = await mysql_data_manager.get_available_tables()
        # 提取表名列表，保持与SQLite API一致的格式
        table_names = [table["table_name"] for table in tables_info]
        return {
            "success": True,
            "message": "获取数据表列表成功",
            "data": table_names
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取数据表列表失败: {str(e)}")

async def get_mysql_data(table: str, page: int = 1, page_size: int = 30, task_times_id: Optional[str] = None):
    """获取MySQL表格数据"""
    try:
        if page < 1:
            page = 1
        if page_size < 1 or page_size > 1000:
            page_size = 30
            
        data = await mysql_data_manager.get_table_data(table, page, page_size, task_times_id)
        return {
            "success": True,
            "message": "获取数据成功",
            "data": data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取数据失败: {str(e)}")

async def get_mysql_stats():
    """获取MySQL数据统计"""
    try:
        stats = await mysql_data_manager.get_data_statistics()
        return {
            "success": True,
            "message": "获取统计数据成功",
            "data": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计数据失败: {str(e)}")

async def export_mysql_data(table_name: str, task_id: Optional[str] = None):
    """导出MySQL表格数据为CSV"""
    return await mysql_data_manager.export_table_data(table_name, task_id)

async def export_mysql_data_as_json(table_name: str, task_id: Optional[str] = None):
    """导出MySQL表格数据为JSON"""
    return await mysql_data_manager.export_table_data_as_json(table_name, task_id)

def get_mysql_table_configs():
    """获取MySQL表格配置信息"""
    return mysql_data_manager.table_configs

# 任务管理API函数
async def create_mysql_task(task_times_id: str, task_data: Dict[str, Any]):
    """创建MySQL任务记录"""
    return await mysql_data_manager.create_task(task_times_id, task_data)

async def get_mysql_task(task_times_id: str):
    """获取MySQL任务信息"""
    return await mysql_data_manager.get_task(task_times_id)

async def update_mysql_task_status(task_times_id: str, status: str, message: str, result: Optional[Dict] = None):
    """更新MySQL任务状态"""
    return await mysql_data_manager.update_task_status(task_times_id, status, message, result)

async def get_all_mysql_tasks(page: int = 1, page_size: int = 30):
    """获取所有MySQL任务"""
    db = await mysql_data_manager.get_connection()
    
    try:
        # 计算偏移量
        offset = (page - 1) * page_size
        
        # 获取总数
        total_result = await db.query("SELECT COUNT(*) as total FROM crawler_tasks")
        total = total_result[0]['total'] if total_result else 0
        
        # 获取分页数据
        tasks = await db.query(
            "SELECT * FROM crawler_tasks ORDER BY created_at DESC LIMIT %s OFFSET %s",
            page_size, offset
        )
        
        # 处理任务数据
        processed_tasks = []
        for task in tasks:
            # 处理结果字段
            if task.get('result_stdout') or task.get('result_stderr'):
                task['result'] = {
                    'stdout': task.get('result_stdout'),
                    'stderr': task.get('result_stderr')
                }
            
            # 处理时间字段
            for time_field in ['created_at', 'updated_at']:
                if task.get(time_field) and isinstance(task[time_field], datetime):
                    task[time_field] = task[time_field].isoformat()
            
            processed_tasks.append(task)
        
        return {
            "tasks": processed_tasks,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取MySQL任务列表失败: {str(e)}")

async def delete_mysql_task(task_times_id: str):
    """删除MySQL任务"""
    return await mysql_data_manager.delete_task(task_times_id)

# 清理函数
async def cleanup_mysql_connections():
    """清理MySQL连接"""
    await mysql_data_manager.close_connection()