#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速数据库分析脚本
用于快速查看SQLite数据库的表结构
"""

import sqlite3
import sys
import os


def quick_analyze(db_path: str):
    """快速分析数据库结构"""
    if not os.path.exists(db_path):
        print(f"❌ 数据库文件不存在: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"📊 数据库文件: {db_path}")
        print("=" * 80)
        
        # 获取所有表
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"\n📋 发现 {len(tables)} 个数据表:")
        print("-" * 40)
        
        for i, table_name in enumerate(tables, 1):
            # 获取行数
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = cursor.fetchone()[0]
            
            # 获取列信息
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print(f"{i:2d}. {table_name:<30} ({row_count:>8} 行, {len(columns):>2} 列)")
        
        print("\n" + "=" * 80)
        
        # 详细表结构
        for table_name in tables:
            print(f"\n📋 表: {table_name}")
            print("-" * 60)
            
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print(f"{'序号':<4} {'字段名':<20} {'类型':<15} {'非空':<6} {'主键':<6} {'默认值':<10}")
            print("-" * 60)
            
            for col in columns:
                cid, name, col_type, notnull, default_value, pk = col
                notnull_str = "是" if notnull else "否"
                pk_str = "是" if pk else "否"
                default_str = str(default_value) if default_value is not None else ""
                
                print(f"{cid+1:<4} {name:<20} {col_type:<15} {notnull_str:<6} {pk_str:<6} {default_str:<10}")
            
            # 获取索引信息
            cursor.execute(f"PRAGMA index_list({table_name})")
            indexes = cursor.fetchall()
            
            if indexes:
                print(f"\n📊 索引信息:")
                for idx in indexes:
                    index_name = idx[1]
                    unique = "唯一" if idx[2] else "普通"
                    
                    cursor.execute(f"PRAGMA index_info({index_name})")
                    index_columns = [col[2] for col in cursor.fetchall()]
                    
                    if not index_name.startswith('sqlite_autoindex'):
                        print(f"  - {index_name} ({unique}): {', '.join(index_columns)}")
        
        conn.close()
        print(f"\n✅ 分析完成")
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")


if __name__ == "__main__":
    # 默认数据库路径
    default_db = "../data/mc.db"
    
    # 从命令行参数获取数据库路径
    db_path = sys.argv[1] if len(sys.argv) > 1 else default_db
    
    quick_analyze(db_path)