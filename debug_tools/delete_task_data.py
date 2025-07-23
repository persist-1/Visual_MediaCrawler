#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务数据删除调试脚本
根据task_times_id删除相关联的所有数据表记录

使用方法:
    python delete_task_data.py

功能:
    1. 选择数据库类型（SQLite/MySQL）
    2. 输入task_times_id
    3. 删除相关数据并显示统计信息
"""

import asyncio
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    import aiosqlite
    import aiomysql
except ImportError:
    print("请安装必要的依赖: pip install aiosqlite aiomysql")
    sys.exit(1)

from config.base_config import *
from config.db_config import *


class TaskDataDeleter:
    """任务数据删除器"""
    
    def __init__(self):
        # 定义所有包含task_times_id字段的表
        self.tables_with_task_id = [
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
            'zhihu_creator',
            'crawler_tasks'
        ]
        
        self.deletion_stats = {}
    
    async def get_sqlite_connection(self):
        """获取SQLite数据库连接"""
        # 尝试多个可能的数据库路径
        possible_paths = [
            project_root / "schema" / "sqlite_tables.db",  # 配置文件中的默认路径
            project_root / "data" / "mc.db",              # 文档中提到的路径
            project_root / "data" / "media_crawler.db",   # 原始路径
            project_root / "media_crawler.db"              # 根目录下的备用路径
        ]
        
        for db_path in possible_paths:
            if db_path.exists():
                print(f"✓ 找到数据库文件: {db_path}")
                return await aiosqlite.connect(str(db_path))
        
        # 如果都没找到，显示详细的错误信息
        error_msg = f"SQLite数据库文件未找到，已尝试以下路径:\n"
        for path in possible_paths:
            error_msg += f"  - {path} {'(存在)' if path.exists() else '(不存在)'}\n"
        error_msg += "\n请确保数据库文件存在，或运行爬虫程序生成数据库文件。"
        raise FileNotFoundError(error_msg)
    
    async def get_mysql_connection(self):
        """获取MySQL数据库连接"""
        try:
            connection = await aiomysql.connect(
                host=MYSQL_DB_HOST,
                port=MYSQL_DB_PORT,
                user=MYSQL_DB_USER,
                password=MYSQL_DB_PWD,
                db=MYSQL_DB_NAME,
                charset='utf8mb4'
            )
            return connection
        except Exception as e:
            raise ConnectionError(f"MySQL连接失败: {e}")
    
    async def count_records_sqlite(self, db, table: str, task_times_id: str) -> int:
        """统计SQLite表中的记录数"""
        try:
            # 检查表是否存在
            cursor = await db.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?", 
                (table,)
            )
            table_exists = await cursor.fetchone()
            
            if not table_exists:
                return 0
            
            # 检查表是否有task_times_id字段
            cursor = await db.execute(f"PRAGMA table_info({table})")
            columns = await cursor.fetchall()
            has_task_times_id = any(col[1] == 'task_times_id' for col in columns)
            
            if not has_task_times_id:
                return 0
            
            # 统计记录数
            cursor = await db.execute(
                f"SELECT COUNT(*) FROM {table} WHERE task_times_id = ?", 
                (task_times_id,)
            )
            result = await cursor.fetchone()
            return result[0] if result else 0
            
        except Exception as e:
            print(f"统计表 {table} 记录数时出错: {e}")
            return 0
    
    async def count_records_mysql(self, cursor, table: str, task_times_id: str) -> int:
        """统计MySQL表中的记录数"""
        try:
            # 检查表是否存在
            await cursor.execute(
                "SELECT COUNT(*) as count FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = %s",
                (table,)
            )
            table_check_result = await cursor.fetchone()
            
            if not table_check_result or table_check_result['count'] == 0:
                return 0
            
            # 检查表是否有task_times_id字段
            await cursor.execute(
                "SELECT COUNT(*) as count FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = %s AND column_name = 'task_times_id'",
                (table,)
            )
            column_check_result = await cursor.fetchone()
            
            if not column_check_result or column_check_result['count'] == 0:
                return 0
            
            # 统计记录数
            await cursor.execute(
                f"SELECT COUNT(*) as count FROM `{table}` WHERE task_times_id = %s",
                (task_times_id,)
            )
            result = await cursor.fetchone()
            return result['count'] if result else 0
            
        except Exception as e:
            print(f"统计表 {table} 记录数时出错: {e}")
            return 0
    
    async def delete_task_data_sqlite(self, task_times_id: str, dry_run: bool = False):
        """删除SQLite中的任务数据"""
        db = await self.get_sqlite_connection()
        
        try:
            print(f"\n{'=' * 50}")
            print(f"SQLite数据库 - 任务ID: {task_times_id}")
            print(f"{'=' * 50}")
            
            total_records = 0
            
            # 统计和删除数据
            for table in self.tables_with_task_id:
                count = await self.count_records_sqlite(db, table, task_times_id)
                
                if count > 0:
                    self.deletion_stats[table] = count
                    total_records += count
                    
                    if not dry_run:
                        try:
                            await db.execute(
                                f"DELETE FROM {table} WHERE task_times_id = ?", 
                                (task_times_id,)
                            )
                            print(f"✓ 已删除表 {table:<25} 记录数: {count:>6}")
                        except Exception as e:
                            print(f"✗ 删除表 {table} 失败: {e}")
                    else:
                        print(f"○ 预览表 {table:<25} 记录数: {count:>6}")
            
            if not dry_run:
                await db.commit()
                print(f"\n✓ 删除完成! 总计删除 {total_records} 条记录")
            else:
                print(f"\n○ 预览完成! 总计将删除 {total_records} 条记录")
            
        except Exception as e:
            print(f"删除SQLite数据时出错: {e}")
        finally:
            await db.close()
    
    async def delete_task_data_mysql(self, task_times_id: str, dry_run: bool = False):
        """删除MySQL中的任务数据"""
        connection = await self.get_mysql_connection()
        
        try:
            cursor = await connection.cursor(aiomysql.DictCursor)
            
            print(f"\n{'=' * 50}")
            print(f"MySQL数据库 - 任务ID: {task_times_id}")
            print(f"{'=' * 50}")
            
            total_records = 0
            
            # 统计和删除数据
            for table in self.tables_with_task_id:
                count = await self.count_records_mysql(cursor, table, task_times_id)
                
                if count > 0:
                    self.deletion_stats[table] = count
                    total_records += count
                    
                    if not dry_run:
                        try:
                            await cursor.execute(
                                f"DELETE FROM `{table}` WHERE task_times_id = %s", 
                                (task_times_id,)
                            )
                            print(f"✓ 已删除表 {table:<25} 记录数: {count:>6}")
                        except Exception as e:
                            print(f"✗ 删除表 {table} 失败: {e}")
                    else:
                        print(f"○ 预览表 {table:<25} 记录数: {count:>6}")
            
            if not dry_run:
                await connection.commit()
                print(f"\n✓ 删除完成! 总计删除 {total_records} 条记录")
            else:
                print(f"\n○ 预览完成! 总计将删除 {total_records} 条记录")
            
        except Exception as e:
            print(f"删除MySQL数据时出错: {e}")
        finally:
            connection.close()
    
    def print_summary(self):
        """打印删除统计摘要"""
        if not self.deletion_stats:
            print("\n没有找到相关数据")
            return
        
        print(f"\n{'=' * 60}")
        print("删除统计摘要")
        print(f"{'=' * 60}")
        
        total = 0
        for table, count in sorted(self.deletion_stats.items()):
            print(f"{table:<30} {count:>6} 条")
            total += count
        
        print(f"{'-' * 60}")
        print(f"{'总计':<30} {total:>6} 条")
        print(f"{'=' * 60}")


def get_user_input():
    """获取用户输入"""
    print("\n任务数据删除调试工具")
    print("=" * 30)
    
    # 选择数据库类型
    while True:
        print("\n请选择数据库类型:")
        print("1. SQLite")
        print("2. MySQL")
        choice = input("请输入选择 (1/2): ").strip()
        
        if choice == '1':
            db_type = 'sqlite'
            break
        elif choice == '2':
            db_type = 'mysql'
            break
        else:
            print("无效选择，请重新输入")
    
    # 输入task_times_id
    while True:
        task_times_id = input("\n请输入task_times_id: ").strip()
        if task_times_id:
            break
        else:
            print("task_times_id不能为空，请重新输入")
    
    # 选择操作模式
    while True:
        print("\n请选择操作模式:")
        print("1. 预览模式 (只查看，不删除)")
        print("2. 删除模式 (实际删除数据)")
        mode_choice = input("请输入选择 (1/2): ").strip()
        
        if mode_choice == '1':
            dry_run = True
            break
        elif mode_choice == '2':
            # 二次确认
            confirm = input(f"\n⚠️  确认要删除task_times_id为 '{task_times_id}' 的所有相关数据吗？(yes/no): ").strip().lower()
            if confirm in ['yes', 'y']:
                dry_run = False
                break
            else:
                print("操作已取消")
                return None, None, None
        else:
            print("无效选择，请重新输入")
    
    return db_type, task_times_id, dry_run


async def main():
    """主函数"""
    try:
        # 获取用户输入
        result = get_user_input()
        if result[0] is None:
            return
        
        db_type, task_times_id, dry_run = result
        
        # 创建删除器实例
        deleter = TaskDataDeleter()
        
        # 执行删除操作
        if db_type == 'sqlite':
            await deleter.delete_task_data_sqlite(task_times_id, dry_run)
        else:
            await deleter.delete_task_data_mysql(task_times_id, dry_run)
        
        # 打印统计摘要
        deleter.print_summary()
        
    except KeyboardInterrupt:
        print("\n操作已取消")
    except Exception as e:
        print(f"\n程序执行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())