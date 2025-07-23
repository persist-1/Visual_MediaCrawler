#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量任务数据删除脚本
支持从文件读取多个task_times_id进行批量删除

使用方法:
    python batch_delete_tasks.py --db sqlite --file task_ids.txt --preview
    python batch_delete_tasks.py --db mysql --file task_ids.txt --delete

文件格式:
    每行一个task_times_id，支持注释行（以#开头）
    
    示例文件内容:
    # 需要删除的任务ID列表
    20240101_123456
    20240102_234567
    # 这是注释行
    20240103_345678
"""

import argparse
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 导入删除器类
try:
    from delete_task_data import TaskDataDeleter
except ImportError:
    print("错误: 无法导入 TaskDataDeleter 类")
    print("请确保 delete_task_data.py 文件存在且可访问")
    sys.exit(1)


def read_task_ids_from_file(file_path: str) -> list:
    """从文件读取task_times_id列表"""
    task_ids = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # 跳过空行和注释行
                if not line or line.startswith('#'):
                    continue
                
                # 验证task_id格式（简单验证）
                if len(line) > 0:
                    task_ids.append(line)
                else:
                    print(f"警告: 第{line_num}行的task_id格式可能不正确: {line}")
        
        return task_ids
    
    except FileNotFoundError:
        print(f"错误: 文件 '{file_path}' 不存在")
        return []
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return []


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='批量删除任务数据工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  预览批量删除:
    python batch_delete_tasks.py --db sqlite --file task_ids.txt --preview
  
  执行批量删除:
    python batch_delete_tasks.py --db mysql --file task_ids.txt --delete

文件格式:
  每行一个task_times_id，支持#开头的注释行
  
  示例:
    # 需要删除的任务
    20240101_123456
    20240102_234567
        """
    )
    
    parser.add_argument(
        '--db', 
        choices=['sqlite', 'mysql'], 
        required=True,
        help='数据库类型 (sqlite/mysql)'
    )
    
    parser.add_argument(
        '--file', 
        required=True,
        help='包含task_times_id列表的文件路径'
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
    
    parser.add_argument(
        '--max-concurrent', 
        type=int,
        default=3,
        help='最大并发删除数量 (默认: 3)'
    )
    
    return parser.parse_args()


async def process_single_task(deleter: TaskDataDeleter, db_type: str, task_id: str, dry_run: bool, semaphore):
    """处理单个任务的删除"""
    async with semaphore:
        try:
            print(f"\n开始处理任务: {task_id}")
            
            if db_type == 'sqlite':
                await deleter.delete_task_data_sqlite(task_id, dry_run)
            else:
                await deleter.delete_task_data_mysql(task_id, dry_run)
            
            print(f"任务 {task_id} 处理完成")
            return True
            
        except Exception as e:
            print(f"处理任务 {task_id} 时出错: {e}")
            return False


async def main():
    """主函数"""
    try:
        args = parse_arguments()
        
        # 读取任务ID列表
        task_ids = read_task_ids_from_file(args.file)
        
        if not task_ids:
            print("没有找到有效的task_times_id")
            return
        
        print(f"找到 {len(task_ids)} 个任务ID:")
        for i, task_id in enumerate(task_ids, 1):
            print(f"  {i:2d}. {task_id}")
        
        # 确定操作模式
        dry_run = args.preview
        
        # 删除模式下的确认
        if args.delete and not args.force:
            print(f"\n⚠️  警告: 即将删除数据库 '{args.db}' 中 {len(task_ids)} 个任务的所有相关数据!")
            confirm = input("确认继续吗？(yes/no): ").strip().lower()
            if confirm not in ['yes', 'y']:
                print("操作已取消")
                return
        
        # 创建信号量控制并发数
        semaphore = asyncio.Semaphore(args.max_concurrent)
        
        # 批量处理
        print(f"\n{'=' * 60}")
        print(f"开始批量处理 - 数据库: {args.db.upper()}, 模式: {'预览' if dry_run else '删除'}")
        print(f"{'=' * 60}")
        
        # 为每个任务创建删除器实例（避免统计数据混乱）
        tasks = []
        deleters = []
        
        for task_id in task_ids:
            deleter = TaskDataDeleter()
            deleters.append(deleter)
            task = process_single_task(deleter, args.db, task_id, dry_run, semaphore)
            tasks.append(task)
        
        # 等待所有任务完成
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 统计结果
        success_count = sum(1 for result in results if result is True)
        failed_count = len(results) - success_count
        
        print(f"\n{'=' * 60}")
        print("批量处理完成")
        print(f"{'=' * 60}")
        print(f"总任务数: {len(task_ids)}")
        print(f"成功: {success_count}")
        print(f"失败: {failed_count}")
        
        # 汇总统计信息
        if success_count > 0:
            print(f"\n{'=' * 60}")
            print("汇总统计信息")
            print(f"{'=' * 60}")
            
            total_stats = {}
            for deleter in deleters:
                for table, count in deleter.deletion_stats.items():
                    total_stats[table] = total_stats.get(table, 0) + count
            
            if total_stats:
                grand_total = 0
                for table, count in sorted(total_stats.items()):
                    print(f"{table:<30} {count:>6} 条")
                    grand_total += count
                
                print(f"{'-' * 60}")
                print(f"{'总计':<30} {grand_total:>6} 条")
            else:
                print("没有找到相关数据")
        
    except KeyboardInterrupt:
        print("\n操作已取消")
    except Exception as e:
        print(f"\n程序执行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())