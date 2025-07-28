#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库表结构更新脚本

功能说明：
1. 连接MySQL和SQLite数据库，查询现有表结构
2. 解析schema目录下的SQL文件，获取标准表结构定义
3. 对比实际表结构与标准定义，识别缺失的字段
4. 自动执行ALTER TABLE语句，为缺失字段添加到数据库表中
5. 支持MySQL和SQLite两种数据库类型
6. 提供详细的操作日志和错误处理

使用方法：
    python update_db.py [--db-type mysql|sqlite|all] [--dry-run]

参数说明：
    --db-type: 指定要更新的数据库类型，默认为all
    --dry-run: 仅显示需要执行的SQL语句，不实际执行

注意事项：
- 执行前请备份数据库
- 建议先使用--dry-run参数预览要执行的操作
- 确保数据库连接配置正确

作者: persist-1 <persist1@126.com>
编写时间: 2025/7/29 1:46
"""

import os
import sys
import re
import argparse
import logging
from typing import Dict, List, Tuple, Optional
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

try:
    import asyncio
    import aiomysql
    import aiosqlite
    from config.db_config import *
except ImportError as e:
    print(f"导入依赖失败: {e}")
    print("请确保已安装必要的依赖包: aiomysql, aiosqlite")
    sys.exit(1)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('update_db.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


class DatabaseUpdater:
    """数据库表结构更新器"""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.schema_dir = project_root / "schema"
        self.mysql_schema_file = self.schema_dir / "mysql_tables.sql"
        self.sqlite_schema_file = self.schema_dir / "sqlite_tables.sql"
        
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
            logger.error(f"MySQL连接失败: {e}")
            return None
    
    async def get_sqlite_connection(self):
        """获取SQLite数据库连接"""
        try:
            db_path = project_root / SQLITE_DB_PATH
            connection = await aiosqlite.connect(str(db_path))
            return connection
        except Exception as e:
            logger.error(f"SQLite连接失败: {e}")
            return None
    
    def parse_sql_schema(self, sql_file: Path, db_type: str) -> Dict[str, List[Dict]]:
        """解析SQL文件，提取表结构定义"""
        if not sql_file.exists():
            logger.error(f"Schema文件不存在: {sql_file}")
            return {}
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tables = {}
        
        # 匹配CREATE TABLE语句 - 支持MySQL和SQLite格式
        if db_type == 'mysql':
            # MySQL格式：以ENGINE结尾
            create_table_pattern = r'CREATE TABLE `?([^`\s]+)`?\s*\(((?:[^()]|\([^)]*\))*)\)\s*ENGINE'
        else:
            # SQLite格式：以分号结尾或下一个语句开始
            create_table_pattern = r'CREATE TABLE `?([^`\s]+)`?\s*\(((?:[^()]|\([^)]*\))*)\)\s*;'
        matches = re.finditer(create_table_pattern, content, re.DOTALL | re.IGNORECASE)
        
        for match in matches:
            table_name = match.group(1)
            table_def = match.group(2)
            
            columns = self._parse_table_columns(table_def, db_type)
            if columns:
                tables[table_name] = columns
                logger.debug(f"解析表 {table_name}: {len(columns)} 个字段")
        
        logger.info(f"从 {sql_file.name} 解析到 {len(tables)} 个表")
        return tables
    
    def _parse_table_columns(self, table_def: str, db_type: str) -> List[Dict]:
        """解析表定义中的列信息"""
        columns = []
        lines = table_def.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 跳过约束定义行
            if (line.startswith('PRIMARY KEY') or line.startswith('KEY') or 
                line.startswith('INDEX') or line.startswith('UNIQUE') or
                line.startswith('CONSTRAINT') or line.upper().startswith('KEY')):
                continue
            
            # 移除末尾的逗号
            line = line.rstrip(',')
            
            # 解析列定义 - 只匹配以反引号或字母开头的列定义
            column_match = re.match(r'`([^`]+)`\s+(.+)', line)
            if not column_match:
                # 尝试匹配不带反引号的列名
                column_match = re.match(r'([a-zA-Z_][a-zA-Z0-9_]*)\s+(.+)', line)
            
            if column_match:
                column_name = column_match.group(1)
                column_def = column_match.group(2).strip()
                
                # 跳过约束定义
                if column_name.upper() in ['PRIMARY', 'KEY', 'INDEX', 'CONSTRAINT', 'UNIQUE']:
                    continue
                
                columns.append({
                    'name': column_name,
                    'definition': column_def,
                    'full_line': line
                })
        
        return columns
    
    async def get_mysql_table_columns(self, connection, table_name: str) -> List[str]:
        """获取MySQL表的现有列名"""
        try:
            async with connection.cursor() as cursor:
                await cursor.execute(f"DESCRIBE `{table_name}`")
                result = await cursor.fetchall()
                return [row[0] for row in result]
        except Exception as e:
            logger.warning(f"获取MySQL表 {table_name} 结构失败: {e}")
            return []
    
    async def get_sqlite_table_columns(self, connection, table_name: str) -> List[str]:
        """获取SQLite表的现有列名"""
        try:
            async with connection.execute(f"PRAGMA table_info(`{table_name}`);") as cursor:
                result = await cursor.fetchall()
                return [row[1] for row in result]
        except Exception as e:
            logger.warning(f"获取SQLite表 {table_name} 结构失败: {e}")
            return []
    
    async def update_mysql_tables(self):
        """更新MySQL表结构"""
        logger.info("开始更新MySQL表结构...")
        
        connection = await self.get_mysql_connection()
        if not connection:
            return False
        
        try:
            schema_tables = self.parse_sql_schema(self.mysql_schema_file, 'mysql')
            success_count = 0
            
            for table_name, schema_columns in schema_tables.items():
                existing_columns = await self.get_mysql_table_columns(connection, table_name)
                
                if not existing_columns:
                    logger.warning(f"MySQL表 {table_name} 不存在，跳过")
                    continue
                
                missing_columns = []
                for col in schema_columns:
                    if col['name'] not in existing_columns:
                        missing_columns.append(col)
                
                if missing_columns:
                    logger.info(f"MySQL表 {table_name} 需要添加 {len(missing_columns)} 个字段")
                    
                    for col in missing_columns:
                        alter_sql = f"ALTER TABLE `{table_name}` ADD COLUMN `{col['name']}` {col['definition']}"
                        
                        if self.dry_run:
                            logger.info(f"[DRY-RUN] {alter_sql}")
                        else:
                            try:
                                async with connection.cursor() as cursor:
                                    await cursor.execute(alter_sql)
                                    await connection.commit()
                                logger.info(f"✓ 成功添加字段: {table_name}.{col['name']}")
                                success_count += 1
                            except Exception as e:
                                logger.error(f"✗ 添加字段失败 {table_name}.{col['name']}: {e}")
                else:
                    logger.info(f"MySQL表 {table_name} 结构已是最新")
            
            if not self.dry_run:
                logger.info(f"MySQL表结构更新完成，成功添加 {success_count} 个字段")
            return True
            
        except Exception as e:
            logger.error(f"更新MySQL表结构时发生错误: {e}")
            return False
        finally:
            connection.close()
    
    async def update_sqlite_tables(self):
        """更新SQLite表结构"""
        logger.info("开始更新SQLite表结构...")
        
        connection = await self.get_sqlite_connection()
        if not connection:
            return False
        
        try:
            schema_tables = self.parse_sql_schema(self.sqlite_schema_file, 'sqlite')
            success_count = 0
            
            for table_name, schema_columns in schema_tables.items():
                existing_columns = await self.get_sqlite_table_columns(connection, table_name)
                
                if not existing_columns:
                    logger.warning(f"SQLite表 {table_name} 不存在，跳过")
                    continue
                
                missing_columns = []
                for col in schema_columns:
                    if col['name'] not in existing_columns:
                        missing_columns.append(col)
                
                if missing_columns:
                    logger.info(f"SQLite表 {table_name} 需要添加 {len(missing_columns)} 个字段")
                    
                    for col in missing_columns:
                        alter_sql = f"ALTER TABLE `{table_name}` ADD COLUMN `{col['name']}` {col['definition']}"
                        
                        if self.dry_run:
                            logger.info(f"[DRY-RUN] {alter_sql}")
                        else:
                            try:
                                await connection.execute(alter_sql)
                                await connection.commit()
                                logger.info(f"✓ 成功添加字段: {table_name}.{col['name']}")
                                success_count += 1
                            except Exception as e:
                                logger.error(f"✗ 添加字段失败 {table_name}.{col['name']}: {e}")
                else:
                    logger.info(f"SQLite表 {table_name} 结构已是最新")
            
            if not self.dry_run:
                logger.info(f"SQLite表结构更新完成，成功添加 {success_count} 个字段")
            return True
            
        except Exception as e:
            logger.error(f"更新SQLite表结构时发生错误: {e}")
            return False
        finally:
            await connection.close()
    
    async def run(self, db_type: str = 'all'):
        """运行数据库更新"""
        logger.info(f"开始数据库表结构更新任务 (类型: {db_type}, 模式: {'预览' if self.dry_run else '执行'})")
        
        success = True
        
        if db_type in ['mysql', 'all']:
            mysql_success = await self.update_mysql_tables()
            success = success and mysql_success
        
        if db_type in ['sqlite', 'all']:
            sqlite_success = await self.update_sqlite_tables()
            success = success and sqlite_success
        
        if success:
            logger.info("数据库表结构更新任务完成")
        else:
            logger.error("数据库表结构更新任务存在错误")
        
        return success


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='数据库表结构更新脚本')
    parser.add_argument(
        '--db-type',
        choices=['mysql', 'sqlite', 'all'],
        default='all',
        help='指定要更新的数据库类型 (默认: all)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='仅显示需要执行的SQL语句，不实际执行'
    )
    
    args = parser.parse_args()
    
    # 创建更新器实例
    updater = DatabaseUpdater(dry_run=args.dry_run)
    
    # 运行更新任务
    try:
        success = asyncio.run(updater.run(args.db_type))
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("用户中断操作")
        sys.exit(1)
    except Exception as e:
        logger.error(f"程序执行出错: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()