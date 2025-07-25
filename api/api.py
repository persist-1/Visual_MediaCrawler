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
import subprocess
import sys
from typing import Optional, Literal
from pathlib import Path
import json
import os
from datetime import datetime

# 动态添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi import HTTPException, BackgroundTasks, Query, APIRouter, Body
from fastapi_offline import FastAPIOffline as FastAPI
from pydantic import BaseModel, Field
import uvicorn
try:
    from .extra_sqlite_api import (
        get_sqlite_tables,
        get_sqlite_data,
        get_sqlite_stats,
        export_sqlite_data,
        export_sqlite_data_as_json,
        get_table_configs,
        create_task,
        get_task,
        update_task_status,
        get_all_tasks,
        delete_task as db_delete_task
    )
    from .extra_mysql_api import (
        get_mysql_tables,
        get_mysql_data,
        get_mysql_stats,
        export_mysql_data,
        export_mysql_data_as_json,
        get_mysql_table_configs,
        create_mysql_task,
        get_mysql_task,
        update_mysql_task_status,
        get_all_mysql_tasks,
        delete_mysql_task,
        cleanup_mysql_connections
    )
    from .static_page_api import create_integrated_app
except ImportError:
    from extra_sqlite_api import (
        get_sqlite_tables,
        get_sqlite_data,
        get_sqlite_stats,
        export_sqlite_data,
        export_sqlite_data_as_json,
        get_table_configs,
        create_task,
        get_task,
        update_task_status,
        get_all_tasks,
        delete_task as db_delete_task
    )
    from extra_mysql_api import (
        get_mysql_tables,
        get_mysql_data,
        get_mysql_stats,
        export_mysql_data,
        export_mysql_data_as_json,
        get_mysql_table_configs,
        create_mysql_task,
        get_mysql_task,
        update_mysql_task_status,
        get_all_mysql_tasks,
        delete_mysql_task,
        cleanup_mysql_connections
    )
    from static_page_api import create_integrated_app

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 创建基础FastAPI应用
base_app = FastAPI(
    title="Visual_MediaCrawler(Based on MediaCrawler)",
    description="可视化自媒体平台爬虫API服务",
    version="1.0.0"
)

# 创建API路由器
api_router = APIRouter(prefix="/api")

# 请求模型
class CrawlerRequest(BaseModel):
    """爬虫请求参数模型"""
    platform: Literal["xhs", "dy", "ks", "bili", "wb", "tieba", "zhihu"] = Field(
        default="xhs",
        description="媒体平台选择 (xhs | dy | ks | bili | wb | tieba | zhihu)"
    )
    lt: Literal["qrcode", "phone", "cookie"] = Field(
        default="qrcode",
        description="登录类型 (qrcode | phone | cookie)"
    )
    type: Literal["search", "detail", "creator"] = Field(
        default="search",
        description="爬虫类型 (search | detail | creator)"
    )
    start: Optional[int] = Field(
        default=None,
        description="起始页数",
        ge=1
    )
    max_count: Optional[int] = Field(
        default=None,
        description="最大爬取数量",
        ge=1,
        le=1000
    )
    keywords: Optional[str] = Field(
        default=None,
        description="搜索关键词"
    )
    specified_ids: Optional[list[str]] = Field(
        default=None,
        description="指定的详情页ID/URL列表（用于detail类型）"
    )
    creator_ids: Optional[list[str]] = Field(
        default=None,
        description="指定的创作者ID/URL列表（用于creator类型）"
    )
    get_comment: Optional[bool] = Field(
        default=None,
        description="是否爬取一级评论"
    )
    get_sub_comment: Optional[bool] = Field(
        default=None,
        description="是否爬取二级评论"
    )
    storage_type: Literal["sqlite", "mysql"] = Field(
        default="sqlite",
        description="数据存储类型选择 (sqlite | mysql)"
    )
    cookies: Optional[str] = Field(
        default=None,
        description="用于cookie登录类型的cookies"
    )

# 响应模型
class CrawlerResponse(BaseModel):
    """爬虫响应模型"""
    success: bool = Field(description="执行是否成功")
    message: str = Field(description="响应消息")
    task_times_id: Optional[str] = Field(default=None, description="任务ID（异步执行时返回）")
    data: Optional[dict] = Field(default=None, description="返回数据")

class TaskStatusResponse(BaseModel):
    """任务状态响应模型"""
    task_times_id: str = Field(description="任务ID")
    status: Literal["running", "completed", "failed"] = Field(description="任务状态")
    message: str = Field(description="状态消息")
    result: Optional[dict] = Field(default=None, description="执行结果")

# 任务管理现在使用数据库，不再需要内存存储和文件操作

async def add_task_info(task_times_id: str, request: CrawlerRequest):
    """添加任务基本信息"""
    task_data = {
        "task_times_id": task_times_id,
        "status": "pending",
        "message": "任务已创建，等待执行",
        "result": None,
        "platform": request.platform,
        "crawler_type": request.type,
        "keywords": request.keywords,
        "login_type": request.lt,
        "start_page": request.start,
        "get_comment": request.get_comment,
        "get_sub_comment": request.get_sub_comment,
        "storage_type": request.storage_type
    }
    
    # 根据存储类型选择对应的数据库创建任务记录
    if request.storage_type == "mysql":
        try:
            await create_mysql_task(task_times_id, task_data)
        except Exception as e:
            print(f"MySQL任务创建失败: {e}")
    else:
        # 默认使用SQLite
        await create_task(task_times_id, task_data)

def bool_to_str(value: Optional[bool]) -> Optional[str]:
    """将布尔值转换为字符串"""
    if value is None:
        return None
    return "true" if value else "false"

def build_command(request: CrawlerRequest, task_times_id: str = None) -> list[str]:
    """构建命令行参数"""
    cmd = [sys.executable, "main.py"]
    
    # 添加平台参数
    cmd.extend(["--platform", request.platform])
    
    # 添加登录类型参数
    cmd.extend(["--lt", request.lt])
    
    # 添加爬虫类型参数
    cmd.extend(["--type", request.type])
    
    # 添加任务ID参数（用于数据追踪）
    if task_times_id is not None:
        cmd.extend(["--task_id", task_times_id])
    
    # 添加可选参数
    if request.start is not None:
        cmd.extend(["--start", str(request.start)])
    
    if request.max_count is not None:
        cmd.extend(["--max_count", str(request.max_count)])
    
    if request.keywords is not None:
        cmd.extend(["--keywords", request.keywords])
    
    # 处理指定ID列表参数
    if request.specified_ids is not None and len(request.specified_ids) > 0:
        cmd.extend(["--specified_ids", ",".join(request.specified_ids)])
    
    if request.creator_ids is not None and len(request.creator_ids) > 0:
        cmd.extend(["--creator_ids", ",".join(request.creator_ids)])
    
    if request.get_comment is not None:
        cmd.extend(["--get_comment", bool_to_str(request.get_comment)])
    
    if request.get_sub_comment is not None:
        cmd.extend(["--get_sub_comment", bool_to_str(request.get_sub_comment)])
    
    # 添加存储类型参数
    cmd.extend(["--storage_type", request.storage_type])
    
    if request.cookies is not None:
        cmd.extend(["--cookies", request.cookies])
    
    return cmd

def _clean_output_text(text: str) -> str:
    """
    清理子进程输出文本中的控制字符和编码问题
    """
    if not text:
        return text
    
    # 移除ANSI控制字符
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    text = ansi_escape.sub('', text)
    
    # 定义已知的乱码到正确文本的映射
    garbled_mappings = {
        'ʹñ׼ģʽ': '使用标准模式',
        '˺δ¼': '账号未登录',
        'ɶľ': '获取视频详情错误',
        'ɶľƵϸ': '获取视频详情',
        'ɶľƵ': '获取视频',
        'ʹñ׼': '使用标准',
        'ģʽ': '模式',
        '˺': '账号',
        'δ¼': '未登录',
        'ɶ': '获取',
        'ľ': '详情',
        'ľ': '错误',
        'ͼƬģʽδ': '图片模式未开启',
        'ͼƬģʽ': '图片模式',
        'δ': '未开启',
    }
    
    # 应用已知的乱码修复映射
    for garbled, correct in garbled_mappings.items():
        if garbled in text:
            text = text.replace(garbled, correct)
    
    # 在Windows系统下，尝试其他编码修复方法
    if sys.platform.startswith('win'):
        # 检查是否还有其他编码问题（如GBK乱码）
        # 寻找可能的中文字符范围外的字符，但看起来像是编码错误的
        if any(ord(char) > 127 and ord(char) < 256 for char in text):
            try:
                # 尝试将文本当作latin1编码的UTF-8字节重新解码
                text_bytes = text.encode('latin1', errors='ignore')
                try:
                    # 尝试用UTF-8解码
                    fixed_text = text_bytes.decode('utf-8', errors='replace')
                    # 验证修复后的文本是否包含中文字符
                    if any('\u4e00' <= char <= '\u9fff' for char in fixed_text):
                        text = fixed_text
                except UnicodeDecodeError:
                    pass
            except (UnicodeEncodeError, UnicodeDecodeError):
                pass
    
    # 移除其他控制字符，但保留换行符和制表符
    text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\t\r')
    
    return text

def _run_subprocess(command: list[str], cwd: str):
    """在线程中执行子进程"""
    import sys
    import os
    
    # 设置环境变量确保输出为UTF-8编码
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    env['PYTHONLEGACYWINDOWSSTDIO'] = '0'  # 禁用Windows传统stdio模式
    
    # Windows系统额外设置
    if sys.platform.startswith('win'):
        env['CHCP'] = '65001'  # 设置控制台代码页为UTF-8
        # 设置Python输出编码
        env['PYTHONIOENCODING'] = 'utf-8:replace'
    
    # 统一使用UTF-8编码，因为MediaCrawler输出的是UTF-8
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            env=env
        )
        return result
    except Exception as e:
        print(f"subprocess执行异常: {e}")
        # 如果UTF-8失败，尝试不指定编码，让系统自动处理
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=False,  # 获取bytes
                env=env
            )
            # 手动处理编码
            stdout_text = ""
            stderr_text = ""
            
            if result.stdout:
                try:
                    stdout_text = result.stdout.decode('utf-8', errors='replace')
                except UnicodeDecodeError:
                    try:
                        stdout_text = result.stdout.decode('gbk', errors='replace')
                    except UnicodeDecodeError:
                        stdout_text = result.stdout.decode('latin1', errors='replace')
            
            if result.stderr:
                try:
                    stderr_text = result.stderr.decode('utf-8', errors='replace')
                except UnicodeDecodeError:
                    try:
                        stderr_text = result.stderr.decode('gbk', errors='replace')
                    except UnicodeDecodeError:
                        stderr_text = result.stderr.decode('latin1', errors='replace')
            
            # 创建一个模拟的result对象
            class MockResult:
                def __init__(self, returncode, stdout, stderr):
                    self.returncode = returncode
                    self.stdout = stdout
                    self.stderr = stderr
            
            return MockResult(result.returncode, stdout_text, stderr_text)
        except Exception as e2:
            print(f"备用编码处理也失败: {e2}")
            raise e

async def run_crawler_task(task_times_id: str, command: list[str], storage_type: str = "sqlite"):
    """异步执行爬虫任务"""
    try:
        print(f"异步任务 {task_times_id} 开始执行命令: {' '.join(command)}")
        
        # 根据存储类型更新任务状态为运行中
        if storage_type == "mysql":
            try:
                await update_mysql_task_status(task_times_id, "running", "任务正在执行中...", None)
            except Exception as e:
                print(f"更新MySQL任务状态失败: {e}")
        else:
            await update_task_status(task_times_id, "running", "任务正在执行中...", None)
        
        # 在线程池中执行命令以避免阻塞事件循环
        import concurrent.futures
        loop = asyncio.get_event_loop()
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(
                executor, 
                _run_subprocess, 
                command, 
                str(PROJECT_ROOT)
            )
        
        stdout_text = _clean_output_text(result.stdout or "")
        stderr_text = _clean_output_text(result.stderr or "")
        
        print(f"异步任务 {task_times_id} 执行完成，退出码: {result.returncode}")
        print(f"异步任务 {task_times_id} stdout: {stdout_text[:200]}..." if len(stdout_text) > 200 else f"异步任务 {task_times_id} stdout: {stdout_text}")
        print(f"异步任务 {task_times_id} stderr: {stderr_text[:200]}..." if len(stderr_text) > 200 else f"异步任务 {task_times_id} stderr: {stderr_text}")
        
        if result.returncode == 0:
            # 任务执行成功
            result_data = {
                "stdout": stdout_text,
                "stderr": stderr_text
            }
            # 根据存储类型更新任务状态
            if storage_type == "mysql":
                try:
                    await update_mysql_task_status(task_times_id, "completed", "任务执行成功", result_data)
                except Exception as e:
                    print(f"MySQL任务状态更新失败: {e}")
            else:
                await update_task_status(task_times_id, "completed", "任务执行成功", result_data)
        else:
            # 任务执行失败
            result_data = {
                "stdout": stdout_text,
                "stderr": stderr_text
            }
            # 根据存储类型更新任务状态
            if storage_type == "mysql":
                try:
                    await update_mysql_task_status(task_times_id, "failed", f"任务执行失败，退出码: {result.returncode}", result_data)
                except Exception as e:
                    print(f"MySQL任务状态更新失败: {e}")
            else:
                await update_task_status(task_times_id, "failed", f"任务执行失败，退出码: {result.returncode}", result_data)
    
    except Exception as e:
        import traceback
        error_detail = f"任务执行异常: {str(e)}\n{traceback.format_exc()}"
        print(f"异步任务 {task_times_id} 异常: {error_detail}")
        # 根据存储类型更新任务状态
        if storage_type == "mysql":
            try:
                await update_mysql_task_status(task_times_id, "failed", error_detail, None)
            except Exception as mysql_e:
                print(f"MySQL任务状态更新失败: {mysql_e}")
        else:
            await update_task_status(task_times_id, "failed", error_detail, None)

@api_router.get("/", summary="API根路径")
async def root():
    """API根路径"""
    return {
        "message": "MediaCrawler API 服务正在运行",
        "version": "1.0.0",
        "docs": "/docs",
        "frontend": "前端静态文件服务已集成"
    }

@api_router.post("/crawler/run", response_model=CrawlerResponse, summary="同步执行爬虫任务")
async def run_crawler_sync(request: CrawlerRequest):
    """同步执行爬虫任务"""
    try:
        # 构建命令
        command = build_command(request)
        print(f"执行命令: {' '.join(command)}")
        
        # 使用改进的subprocess执行函数
        result = _run_subprocess(command, str(PROJECT_ROOT))
        
        stdout_text = _clean_output_text(result.stdout or "")
        stderr_text = _clean_output_text(result.stderr or "")
        
        print(f"命令执行完成，退出码: {result.returncode}")
        print(f"stdout: {stdout_text[:500]}..." if len(stdout_text) > 500 else f"stdout: {stdout_text}")
        print(f"stderr: {stderr_text[:500]}..." if len(stderr_text) > 500 else f"stderr: {stderr_text}")
        
        if result.returncode == 0:
            return CrawlerResponse(
                success=True,
                message="爬虫任务执行成功",
                data={
                    "stdout": stdout_text,
                    "stderr": stderr_text
                }
            )
        else:
            return CrawlerResponse(
                success=False,
                message=f"爬虫任务执行失败，退出码: {result.returncode}",
                data={
                    "stdout": stdout_text,
                    "stderr": stderr_text
                }
            )
    
    except Exception as e:
        import traceback
        error_detail = f"执行爬虫任务时发生错误: {str(e)}\n{traceback.format_exc()}"
        print(f"API异常: {error_detail}")
        raise HTTPException(status_code=500, detail=error_detail)

@api_router.post("/crawler/run-async", response_model=CrawlerResponse, summary="异步执行爬虫任务")
async def run_crawler_async(request: CrawlerRequest, background_tasks: BackgroundTasks):
    """异步执行爬虫任务"""
    try:
        # 生成任务ID
        import uuid
        task_times_id = str(uuid.uuid4())
        
        # 添加任务基本信息
        await add_task_info(task_times_id, request)
        
        # 构建命令（传递task_times_id用于数据追踪）
        command = build_command(request, task_times_id)
        
        # 添加后台任务
        background_tasks.add_task(run_crawler_task, task_times_id, command, request.storage_type)
        
        return CrawlerResponse(
            success=True,
            message="爬虫任务已提交，正在后台执行",
            task_times_id=task_times_id
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"提交爬虫任务时发生错误: {str(e)}")

@api_router.get("/crawler/task/{task_times_id}", summary="查询任务状态")
async def get_task_status(task_times_id: str):
    """查询任务状态"""
    # 先尝试从SQLite获取任务信息
    task_info = await get_task(task_times_id)
    
    # 如果SQLite中没有，尝试从MySQL获取
    if not task_info:
        try:
            task_info = await get_mysql_task(task_times_id)
        except Exception:
            task_info = None
    
    if not task_info:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    return {
        "task_times_id": task_times_id,
        "status": task_info["status"],
        "message": task_info["message"],
        "result": task_info.get("result"),
        "created_at": task_info.get("created_at"),
        "updated_at": task_info.get("updated_at"),
        "formData": {
            "platform": task_info.get("platform"),
            "type": task_info.get("crawler_type"),
            "keywords": task_info.get("keywords"),
            "lt": task_info.get("login_type"),
            "start": task_info.get("start_page"),
            "get_comment": task_info.get("get_comment"),
            "get_sub_comment": task_info.get("get_sub_comment"),
            "storage_type": task_info.get("storage_type")
        }
    }

@api_router.get("/crawler/tasks", summary="获取所有任务列表")
async def get_all_tasks_api(database: str = Query("all", description="数据库选择 (sqlite | mysql | all)")):
    """获取所有任务列表"""
    all_tasks = []
    
    if database == "mysql":
        # 仅从MySQL获取任务
        try:
            mysql_tasks_result = await get_all_mysql_tasks(1, 1000)  # 获取前1000个任务
            mysql_tasks = mysql_tasks_result.get("tasks", [])
            for task in mysql_tasks:
                all_tasks.append({
                    "task_times_id": task["task_times_id"],
                    "status": task["status"],
                    "message": task["message"],
                    "result": task.get("result"),
                    "created_at": task.get("created_at"),
                    "updated_at": task.get("updated_at"),
                    "formData": {
                        "platform": task.get("platform"),
                        "type": task.get("crawler_type"),
                        "keywords": task.get("keywords"),
                        "lt": task.get("login_type"),
                        "start": task.get("start_page"),
                        "get_comment": task.get("get_comment"),
                        "get_sub_comment": task.get("get_sub_comment"),
                        "storage_type": task.get("storage_type", "mysql")
                    }
                })
        except Exception as e:
            print(f"获取MySQL任务失败: {e}")
    elif database == "sqlite":
        # 仅从SQLite获取任务
        try:
            sqlite_tasks_dict = await get_all_tasks()
            for task_id, task_info in sqlite_tasks_dict.items():
                all_tasks.append({
                    "task_times_id": task_id,
                    "status": task_info["status"],
                    "message": task_info["message"],
                    "result": task_info.get("result"),
                    "created_at": task_info.get("created_at"),
                    "updated_at": task_info.get("updated_at"),
                    "formData": {
                        "platform": task_info.get("platform"),
                        "type": task_info.get("crawler_type"),
                        "keywords": task_info.get("keywords"),
                        "lt": task_info.get("login_type"),
                        "start": task_info.get("start_page"),
                        "get_comment": task_info.get("get_comment"),
                        "get_sub_comment": task_info.get("get_sub_comment"),
                        "storage_type": task_info.get("storage_type", "sqlite")
                    }
                })
        except Exception as e:
            print(f"获取SQLite任务失败: {e}")
    else:
        # 获取所有数据库的任务（默认行为）
        # 获取SQLite中的任务
        try:
            sqlite_tasks_dict = await get_all_tasks()
            for task_id, task_info in sqlite_tasks_dict.items():
                all_tasks.append({
                    "task_times_id": task_id,
                    "status": task_info["status"],
                    "message": task_info["message"],
                    "result": task_info.get("result"),
                    "created_at": task_info.get("created_at"),
                    "updated_at": task_info.get("updated_at"),
                    "formData": {
                        "platform": task_info.get("platform"),
                        "type": task_info.get("crawler_type"),
                        "keywords": task_info.get("keywords"),
                        "lt": task_info.get("login_type"),
                        "start": task_info.get("start_page"),
                        "get_comment": task_info.get("get_comment"),
                        "get_sub_comment": task_info.get("get_sub_comment"),
                        "storage_type": task_info.get("storage_type", "sqlite")
                    }
                })
        except Exception as e:
            print(f"获取SQLite任务失败: {e}")
        
        # 获取MySQL中的任务
        try:
            mysql_tasks_result = await get_all_mysql_tasks(1, 1000)  # 获取前1000个任务
            mysql_tasks = mysql_tasks_result.get("tasks", [])
            for task in mysql_tasks:
                all_tasks.append({
                    "task_times_id": task["task_times_id"],
                    "status": task["status"],
                    "message": task["message"],
                    "result": task.get("result"),
                    "created_at": task.get("created_at"),
                    "updated_at": task.get("updated_at"),
                    "formData": {
                        "platform": task.get("platform"),
                        "type": task.get("crawler_type"),
                        "keywords": task.get("keywords"),
                        "lt": task.get("login_type"),
                        "start": task.get("start_page"),
                        "get_comment": task.get("get_comment"),
                        "get_sub_comment": task.get("get_sub_comment"),
                        "storage_type": task.get("storage_type", "mysql")
                    }
                })
        except Exception as e:
            print(f"获取MySQL任务失败: {e}")
    
    # 按创建时间排序（最新的在前）
    all_tasks.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    
    return {"tasks": all_tasks}

@api_router.delete("/crawler/task/{task_times_id}", summary="删除任务记录")
async def delete_task_api(task_times_id: str):
    """删除任务记录"""
    # 先尝试从SQLite获取任务信息
    task_info = await get_task(task_times_id)
    
    # 如果SQLite中没有，尝试从MySQL获取
    if not task_info:
        try:
            task_info = await get_mysql_task(task_times_id)
        except Exception:
            task_info = None
    
    if not task_info:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    # 根据存储类型删除对应数据库中的数据
    storage_type = task_info.get("storage_type", "sqlite")
    
    if storage_type == "mysql":
        try:
            await delete_mysql_task(task_times_id)
            print(f"已删除MySQL中任务 {task_times_id} 的相关数据")
        except Exception as e:
            print(f"删除MySQL数据时出错: {e}")
            raise HTTPException(status_code=500, detail=f"删除MySQL数据失败: {e}")
    else:
        try:
            await db_delete_task(task_times_id)
            print(f"已删除SQLite中任务 {task_times_id} 的相关数据")
        except Exception as e:
            print(f"删除SQLite数据时出错: {e}")
            raise HTTPException(status_code=500, detail=f"删除SQLite数据失败: {e}")
    
    return {"message": f"任务 {task_times_id} 已删除"}

@api_router.get("/health", summary="健康检查")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "message": "API服务运行正常"}

# SQLite数据API路由
@api_router.get("/sqlite/tables", summary="获取SQLite数据表列表")
async def api_get_sqlite_tables():
    """获取可用的SQLite数据表列表"""
    return await get_sqlite_tables()

@api_router.get("/sqlite/data", summary="获取SQLite表格数据")
async def api_get_sqlite_data(
    table: str = Query(..., description="表名"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(30, ge=1, le=1000, description="每页数量"),
    task_times_id: Optional[str] = Query(None, description="任务ID筛选")
):
    """获取SQLite表格数据"""
    return await get_sqlite_data(table, page, page_size, task_times_id)

@api_router.get("/sqlite/stats", summary="获取SQLite数据统计")
async def api_get_sqlite_stats():
    """获取SQLite数据统计信息"""
    return await get_sqlite_stats()

@api_router.get("/sqlite/export", summary="导出SQLite表格数据")
async def api_export_sqlite_data(
    table_name: str = Query(..., description="表名"),
    task_id: Optional[str] = Query(None, description="任务ID筛选")
):
    """导出SQLite表格数据为CSV"""
    return await export_sqlite_data(table_name, task_id)

@api_router.get("/sqlite/export-json", summary="导出SQLite表格数据为JSON")
async def api_export_sqlite_data_json(
    table_name: str = Query(..., description="表名"),
    task_id: Optional[str] = Query(None, description="任务ID筛选")
):
    """导出SQLite表格数据为JSON"""
    return await export_sqlite_data_as_json(table_name, task_id)

@api_router.get("/sqlite/configs", summary="获取表格配置信息")
async def api_get_table_configs():
    """获取表格配置信息"""
    return get_table_configs()

# MySQL数据API路由
@api_router.get("/mysql/tables", summary="获取MySQL数据表列表")
async def api_get_mysql_tables():
    """获取可用的MySQL数据表列表"""
    return await get_mysql_tables()

@api_router.get("/mysql/data", summary="获取MySQL表格数据")
async def api_get_mysql_data(
    table: str = Query(..., description="表名"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(30, ge=1, le=1000, description="每页数量"),
    task_times_id: Optional[str] = Query(None, description="任务ID筛选")
):
    """获取MySQL表格数据"""
    return await get_mysql_data(table, page, page_size, task_times_id)

@api_router.get("/mysql/stats", summary="获取MySQL数据统计")
async def api_get_mysql_stats():
    """获取MySQL数据统计信息"""
    return await get_mysql_stats()

@api_router.get("/mysql/export", summary="导出MySQL表格数据")
async def api_export_mysql_data(
    table_name: str = Query(..., description="表名"),
    task_id: Optional[str] = Query(None, description="任务ID筛选")
):
    """导出MySQL表格数据为CSV"""
    return await export_mysql_data(table_name, task_id)

@api_router.get("/mysql/export-json", summary="导出MySQL表格数据为JSON")
async def api_export_mysql_data_json(
    table_name: str = Query(..., description="表名"),
    task_id: Optional[str] = Query(None, description="任务ID筛选")
):
    """导出MySQL表格数据为JSON"""
    return await export_mysql_data_as_json(table_name, task_id)

@api_router.get("/mysql/configs", summary="获取MySQL表格配置信息")
async def api_get_mysql_table_configs():
    """获取MySQL表格配置信息"""
    return get_mysql_table_configs()

# MySQL任务管理API路由
@api_router.post("/mysql/tasks", summary="创建MySQL任务")
async def api_create_mysql_task(
    task_times_id: str = Query(..., description="任务ID"),
    task_data: dict = Body(..., description="任务数据")
):
    """创建MySQL任务"""
    return await create_mysql_task(task_times_id, task_data)

@api_router.get("/mysql/tasks/{task_times_id}", summary="获取MySQL任务详情")
async def api_get_mysql_task(task_times_id: str):
    """获取MySQL任务详情"""
    return await get_mysql_task(task_times_id)

@api_router.put("/mysql/tasks/{task_times_id}/status", summary="更新MySQL任务状态")
async def api_update_mysql_task_status(
    task_times_id: str,
    status: str = Body(..., description="任务状态"),
    message: str = Body(..., description="状态消息"),
    result: Optional[dict] = Body(None, description="任务结果")
):
    """更新MySQL任务状态"""
    return await update_mysql_task_status(task_times_id, status, message, result)

@api_router.get("/mysql/tasks", summary="获取所有MySQL任务")
async def api_get_all_mysql_tasks(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(30, ge=1, le=1000, description="每页数量")
):
    """获取所有MySQL任务"""
    return await get_all_mysql_tasks(page, page_size)

@api_router.delete("/mysql/tasks/{task_times_id}", summary="删除MySQL任务")
async def api_delete_mysql_task(task_times_id: str):
    """删除MySQL任务"""
    return await delete_mysql_task(task_times_id)

# 将API路由器添加到基础应用
base_app.include_router(api_router)

# 应用关闭时清理资源
@base_app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时清理资源"""
    try:
        await cleanup_mysql_connections()
        print("MySQL连接已清理")
    except Exception as e:
        print(f"MySQL连接清理失败: {e}")

# 集成静态文件服务，创建完整的应用（在API路由添加之后）
app = create_integrated_app(base_app)

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="127.0.0.1",
        port=10001,
        reload=True,
        log_level="info"
    )