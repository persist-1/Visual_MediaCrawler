# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：  
# 1. 不得用于任何商业用途。  
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。  
# 3. 不得进行大规模爬取或对平台造成运营干扰。  
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。   
# 5. 不得用于任何非法或不当的用途。
#   
# 详细许可条款请参阅项目根目录下的LICENSE文件。  
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。  


# -*- coding: utf-8 -*-
# @Author  : relakkes@gmail.com
# @Time    : 2024/4/6 14:54
# @Desc    : mediacrawler db 管理
import asyncio
from typing import Dict
from urllib.parse import urlparse
import os
import sys

import aiofiles
import aiomysql

try:
    import aiosqlite
except ImportError:
    aiosqlite = None

import config
from config.db_config import AsyncMysqlDB, AsyncSqliteDB
from tools import utils
from var import db_conn_pool_var, media_crawler_db_var


async def init_mediacrawler_db(db_type: str = None):
    """
    初始化数据库链接池对象，并将该对象塞给media_crawler_db_var上下文变量
    Args:
        db_type: 数据库类型，可选值为 'sqlite' 或 'mysql'，默认从配置文件读取
    Returns:

    """
    if db_type is None:
        db_type = getattr(config, 'DB_TYPE', 'sqlite').lower()
    else:
        db_type = db_type.lower()
    
    if db_type == 'mysql':
        pool = await aiomysql.create_pool(
            host=config.MYSQL_DB_HOST,
            port=config.MYSQL_DB_PORT,
            user=config.MYSQL_DB_USER,
            password=config.MYSQL_DB_PWD,
            db=config.MYSQL_DB_NAME,
            autocommit=True,
        )
        async_db_obj = AsyncMysqlDB(pool)
        # 将连接池对象和封装的CRUD sql接口对象放到上下文变量中
        db_conn_pool_var.set(pool)
        media_crawler_db_var.set(async_db_obj)
    elif db_type == 'sqlite':
        if AsyncSqliteDB is None:
            raise ImportError("SQLite support is not available. Please install aiosqlite: pip install aiosqlite")
        
        # 确保SQLite数据库目录存在
        db_path = config.SQLITE_DB_PATH
        db_dir = os.path.dirname(db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        
        async_db_obj = AsyncSqliteDB(db_path)
        # SQLite不需要连接池，直接设置数据库对象
        db_conn_pool_var.set(None)
        media_crawler_db_var.set(async_db_obj)
    else:
        raise ValueError(f"Unsupported database type: {db_type}")


async def init_db(db_type: str = None):
    """
    初始化db连接池
    Args:
        db_type: 数据库类型，可选值为 'sqlite' 或 'mysql'，默认从配置文件读取
    Returns:

    """
    if db_type:
        utils.logger.info(f"[init_db] start init mediacrawler {db_type} db connect object")
    else:
        utils.logger.info("[init_db] start init mediacrawler db connect object")
    await init_mediacrawler_db(db_type)
    utils.logger.info("[init_db] end init mediacrawler db connect object")


async def close(db_type: str = None):
    """
    关闭连接池
    Args:
        db_type: 数据库类型，可选值为 'sqlite' 或 'mysql'，默认从配置文件读取
    Returns:

    """
    utils.logger.info("[close] close mediacrawler db pool")
    if db_type is None:
        db_type = getattr(config, 'DB_TYPE', 'sqlite').lower()
    else:
        db_type = db_type.lower()
    
    if db_type == 'mysql':
        db_pool: aiomysql.Pool = db_conn_pool_var.get()
        if db_pool is not None:
            db_pool.close()
            await db_pool.wait_closed()  # 等待连接池完全关闭
    elif db_type == 'sqlite':
        async_db_obj = media_crawler_db_var.get()
        if async_db_obj is not None:
            await async_db_obj.close()


async def check_database_exists(db_type: str) -> bool:
    """
    检查数据库是否存在且已初始化（包含表结构）
    Args:
        db_type: 数据库类型，'sqlite' 或 'mysql'
    Returns:
        bool: 如果数据库存在且已初始化返回True，否则返回False
    """
    try:
        if db_type == 'sqlite':
            db_path = config.SQLITE_DB_PATH
            if not os.path.exists(db_path):
                return False
            
            # 检查SQLite数据库是否包含表
            async with aiosqlite.connect(db_path) as conn:
                cursor = await conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
                )
                tables = await cursor.fetchall()
                return len(tables) > 0
                
        elif db_type == 'mysql':
            # 检查MySQL数据库是否存在且包含表
            try:
                pool = await aiomysql.create_pool(
                    host=config.MYSQL_DB_HOST,
                    port=config.MYSQL_DB_PORT,
                    user=config.MYSQL_DB_USER,
                    password=config.MYSQL_DB_PWD,
                    db=config.MYSQL_DB_NAME,
                    autocommit=True,
                )
                async with pool.acquire() as conn:
                    async with conn.cursor() as cursor:
                        await cursor.execute("SHOW TABLES")
                        tables = await cursor.fetchall()
                        pool.close()
                        return len(tables) > 0
            except Exception:
                return False
                
    except Exception as e:
        utils.logger.error(f"[check_database_exists] Error checking {db_type} database: {e}")
        return False
    
    return False


def get_user_input_db_type() -> str:
    """
    获取用户输入的数据库类型
    Returns:
        str: 用户选择的数据库类型
    """
    print("\n=== 数据库初始化工具 ===")
    print("请选择要初始化的数据库类型：")
    print("1. sqlite - SQLite数据库")
    print("2. mysql - MySQL数据库")
    print("3. config - 使用配置文件默认设置")
    
    while True:
        try:
            choice = input("\n请输入选项 (1/2/3): ").strip()
            
            if choice == '1':
                return 'sqlite'
            elif choice == '2':
                return 'mysql'
            elif choice == '3':
                default_db_type = getattr(config, 'DB_TYPE', 'sqlite').lower()
                print(f"使用配置文件默认数据库类型: {default_db_type}")
                return default_db_type
            else:
                print("无效选项，请输入 1、2 或 3")
        except KeyboardInterrupt:
            print("\n用户取消操作")
            sys.exit(0)
        except Exception as e:
            print(f"输入错误: {e}，请重新输入")


def get_user_force_confirmation(db_type: str) -> bool:
    """
    获取用户是否强制初始化的确认
    Args:
        db_type: 数据库类型
    Returns:
        bool: 用户是否选择强制初始化
    """
    print(f"\n⚠️  检测到 {db_type.upper()} 数据库已存在且包含表结构！")
    print("数据库已完成初始化，继续操作将删除所有现有数据！")
    print("\n请选择操作：")
    print("1. 取消操作，保留现有数据")
    print("2. 强制重新初始化（⚠️ 将删除所有现有数据）")
    
    while True:
        try:
            choice = input("\n请输入选项 (1/2): ").strip()
            
            if choice == '1':
                print("操作已取消，现有数据保持不变。")
                return False
            elif choice == '2':
                # 二次确认
                confirm = input("\n⚠️ 最后确认：您确定要删除所有现有数据并重新初始化吗？(yes/no): ").strip().lower()
                if confirm in ['yes', 'y', '是', '确定']:
                    print("已确认强制初始化，将删除现有数据...")
                    return True
                else:
                    print("操作已取消，现有数据保持不变。")
                    return False
            else:
                print("无效选项，请输入 1 或 2")
        except KeyboardInterrupt:
            print("\n用户取消操作")
            return False
        except Exception as e:
            print(f"输入错误: {e}，请重新输入")


async def init_table_schema(db_type: str = None):
    """
    用来初始化数据库表结构，请在第一次需要创建表结构的时候使用，多次执行该函数会将已有的表以及数据全部删除
    Args:
        db_type: 数据库类型，可选值为 'sqlite' 或 'mysql'，默认从配置文件读取
    Returns:

    """
    if db_type is None:
        db_type = getattr(config, 'DB_TYPE', 'sqlite').lower()
    else:
        db_type = db_type.lower()
        
    # 验证数据库类型
    if db_type not in ['sqlite', 'mysql']:
        raise ValueError(f"Unsupported database type: {db_type}. Supported types: sqlite, mysql")
        
    utils.logger.info(f"[init_table_schema] begin init {db_type} table schema ...")
    
    await init_mediacrawler_db(db_type)
    async_db_obj = media_crawler_db_var.get()
    
    if db_type == 'mysql':
        schema_file = "schema/mysql_tables.sql"
    elif db_type == 'sqlite':
        schema_file = "schema/sqlite_tables.sql"
    
    try:
        async with aiofiles.open(schema_file, mode="r", encoding="utf-8") as f:
            schema_sql = await f.read()
            await async_db_obj.execute(schema_sql)
            utils.logger.info(f"[init_table_schema] {db_type} table schema init successful")
    except FileNotFoundError:
        utils.logger.error(f"[init_table_schema] Schema file not found: {schema_file}")
        raise
    except Exception as e:
        utils.logger.error(f"[init_table_schema] Failed to initialize {db_type} schema: {e}")
        raise
    finally:
        await close(db_type)


async def main():
    """
    主函数，支持命令行参数和交互式输入选择数据库类型
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='数据库初始化工具')
    parser.add_argument('--db-type', choices=['sqlite', 'mysql', 'config'], 
                       help='数据库类型 (sqlite/mysql/config)，config表示使用配置文件默认设置')
    parser.add_argument('--init-schema', action='store_true',
                       help='初始化数据库表结构')
    parser.add_argument('--init-connection', action='store_true',
                       help='仅初始化数据库连接')
    parser.add_argument('--force', action='store_true',
                       help='强制初始化，即使数据库已存在')
    parser.add_argument('--interactive', action='store_true',
                       help='交互式模式，手动选择数据库类型')
    
    args = parser.parse_args()
    
    try:
        # 确定数据库类型
        db_type = None
        
        if args.interactive or (not args.db_type and len(sys.argv) == 1):
            # 交互式模式或无参数运行时
            db_type = get_user_input_db_type()
        elif args.db_type:
            if args.db_type == 'config':
                db_type = getattr(config, 'DB_TYPE', 'sqlite').lower()
                print(f"使用配置文件默认数据库类型: {db_type}")
            else:
                db_type = args.db_type
        else:
            # 默认使用配置文件设置
            db_type = getattr(config, 'DB_TYPE', 'sqlite').lower()
            print(f"使用配置文件默认数据库类型: {db_type}")
        
        # 检查数据库是否已存在
        force_init = args.force
        if not force_init:
            db_exists = await check_database_exists(db_type)
            if db_exists:
                # 如果是交互式模式或无参数运行，提供用户选择
                if args.interactive or (not args.db_type and len(sys.argv) == 1):
                    force_init = get_user_force_confirmation(db_type)
                    if not force_init:
                        return
                else:
                    # 命令行模式，提示使用--force参数
                    print(f"\n⚠️  检测到 {db_type.upper()} 数据库已存在且包含表结构！")
                    print("数据库已完成初始化，无需重复操作。")
                    print("如需强制重新初始化，请使用 --force 参数。")
                    print("注意：强制初始化将删除所有现有数据！")
                    return
        
        # 执行相应操作
        if args.init_schema or (not args.init_connection and not args.init_schema):
            print(f"\n开始初始化 {db_type.upper()} 数据库表结构...")
            utils.logger.info(f"开始初始化数据库表结构，数据库类型: {db_type}")
            await init_table_schema(db_type)
            print(f"✅ {db_type.upper()} 数据库表结构初始化完成！")
            utils.logger.info("数据库表结构初始化完成")
        elif args.init_connection:
            print(f"\n开始初始化 {db_type.upper()} 数据库连接...")
            utils.logger.info(f"开始初始化数据库连接，数据库类型: {db_type}")
            await init_db(db_type)
            print(f"✅ {db_type.upper()} 数据库连接初始化完成！")
            utils.logger.info("数据库连接初始化完成")
            await close()
            
    except KeyboardInterrupt:
        print("\n用户取消操作")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 数据库初始化失败: {e}")
        utils.logger.error(f"数据库初始化失败: {e}")
        raise


if __name__ == '__main__':
    asyncio.run(main())
