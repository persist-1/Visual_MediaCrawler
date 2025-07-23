#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
临时脚本：根据SQL文件创建SQLite数据库
"""

import sqlite3
import os

def create_database_from_sql():
    """根据SQL文件创建数据库"""
    # 数据库路径
    db_path = "d:/A_work/A_trae_alter/MediaCrawler-main/schema/sqlite_tables.db"
    sql_file_path = "d:/A_work/A_trae_alter/MediaCrawler-main/schema/sqlite_tables.sql"
    
    # 如果数据库已存在，删除它
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"已删除现有数据库: {db_path}")
    
    # 创建数据库连接
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 读取SQL文件
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # 分割SQL语句（按分号分割）
        sql_statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        # 执行每个SQL语句
        for i, statement in enumerate(sql_statements):
            # 跳过注释行
            if statement.startswith('--') or not statement:
                continue
            
            try:
                cursor.execute(statement)
                print(f"执行语句 {i+1}: 成功")
            except sqlite3.Error as e:
                print(f"执行语句 {i+1} 失败: {e}")
                print(f"语句内容: {statement[:100]}...")
        
        # 提交事务
        conn.commit()
        print(f"\n✅ 数据库创建成功: {db_path}")
        
        # 验证表是否创建成功
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"\n📊 创建的表数量: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
            
    except Exception as e:
        print(f"❌ 创建数据库失败: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_database_from_sql()