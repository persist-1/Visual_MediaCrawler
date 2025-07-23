#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速任务数据删除脚本
支持命令行参数快速删除指定task_times_id的数据

使用方法:
    python quick_delete_task.py --db sqlite --task-id your_task_id --preview
    python quick_delete_task.py --db mysql --task-id your_task_id --delete

参数说明:
    --db: 数据库类型 (sqlite/mysql)
    --task-id: 任务ID
    --preview: 预览模式，只查看不删除
    --delete: 删除模式，实际删除数据
"""

import argparse
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from delete_task_data import TaskDataDeleter
except ImportError:
    print("错误: 无法导入 TaskDataDeleter 类")
    print("请确保 delete_task_data.py 文件存在且可访问")
    sys.exit(1)


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='快速删除任务数据工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  预览SQLite中的数据:
    python quick_delete_task.py --db sqlite --task-id 20240101_123456 --preview
  
  删除MySQL中的数据:
    python quick_delete_task.py --db mysql --task-id 20240101_123456 --delete
        """
    )
    
    parser.add_argument(
        '--db', 
        choices=['sqlite', 'mysql'], 
        required=True,
        help='数据库类型 (sqlite/mysql)'
    )
    
    parser.add_argument(
        '--task-id', 
        required=True,
        help='要删除的任务ID (task_times_id)'
    )
    
    # 操作模式互斥组
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        '--preview', 
        action='store_true',
        help='预览模式：只查看数据，不执行删除'
    )
    mode_group.add_argument(
        '--delete', 
        action='store_true',
        help='删除模式：实际删除数据'
    )
    
    parser.add_argument(
        '--force', 
        action='store_true',
        help='强制删除，跳过确认提示'
    )
    
    return parser.parse_args()


async def main():
    """主函数"""
    try:
        args = parse_arguments()
        
        # 确定操作模式
        dry_run = args.preview
        
        # 删除模式下的确认
        if args.delete and not args.force:
            print(f"\n⚠️  警告: 即将删除数据库 '{args.db}' 中task_times_id为 '{args.task_id}' 的所有相关数据!")
            confirm = input("确认继续吗？(yes/no): ").strip().lower()
            if confirm not in ['yes', 'y']:
                print("操作已取消")
                return
        
        # 创建删除器实例
        deleter = TaskDataDeleter()
        
        # 执行操作
        if args.db == 'sqlite':
            await deleter.delete_task_data_sqlite(args.task_id, dry_run)
        else:
            await deleter.delete_task_data_mysql(args.task_id, dry_run)
        
        # 打印统计摘要
        deleter.print_summary()
        
    except KeyboardInterrupt:
        print("\n操作已取消")
    except Exception as e:
        print(f"\n程序执行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())