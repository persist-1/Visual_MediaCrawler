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
# @Time    : 2024/4/6 14:21
# @Desc    : 异步SQLite的增删改查封装
import asyncio
import sqlite3
from typing import Any, Dict, List, Union

try:
    import aiosqlite
except ImportError:
    aiosqlite = None


class AsyncSqliteDB:
    def __init__(self, db_path: str) -> None:
        if aiosqlite is None:
            raise ImportError("aiosqlite is required for SQLite support. Please install it with: pip install aiosqlite")
        
        self.__db_path = db_path
        self._lock = asyncio.Lock()

    async def query(self, sql: str, *args: Union[str, int]) -> List[Dict[str, Any]]:
        """
        从给定的 SQL 中查询记录，返回的是一个列表
        :param sql: 查询的sql
        :param args: sql中传递动态参数列表
        :return:
        """
        async with self._lock:
            async with aiosqlite.connect(self.__db_path) as conn:
                conn.row_factory = aiosqlite.Row
                async with conn.execute(sql, args) as cursor:
                    rows = await cursor.fetchall()
                    return [dict(row) for row in rows] if rows else []

    async def get_first(self, sql: str, *args: Union[str, int]) -> Union[Dict[str, Any], None]:
        """
        从给定的 SQL 中查询记录，返回的是符合条件的第一个结果
        :param sql: 查询的sql
        :param args:sql中传递动态参数列表
        :return:
        """
        async with self._lock:
            async with aiosqlite.connect(self.__db_path) as conn:
                conn.row_factory = aiosqlite.Row
                async with conn.execute(sql, args) as cursor:
                    row = await cursor.fetchone()
                    return dict(row) if row else None

    async def item_to_table(self, table_name: str, item: Dict[str, Any]) -> int:
        """
        表中插入数据
        :param table_name: 表名
        :param item: 一条记录的字典信息
        :return:
        """
        fields = list(item.keys())
        values = list(item.values())
        fields = [f'`{field}`' for field in fields]
        fieldstr = ','.join(fields)
        valstr = ','.join(['?' for _ in range(len(item))])
        sql = f"INSERT INTO {table_name} ({fieldstr}) VALUES({valstr})"
        
        async with self._lock:
            async with aiosqlite.connect(self.__db_path) as conn:
                async with conn.execute(sql, values) as cursor:
                    await conn.commit()
                    return cursor.lastrowid

    async def update_table(self, table_name: str, updates: Dict[str, Any], field_where: str,
                           value_where: Union[str, int, float]) -> int:
        """
        更新指定表的记录
        :param table_name: 表名
        :param updates: 需要更新的字段和值的 key - value 映射
        :param field_where: update 语句 where 条件中的字段名
        :param value_where: update 语句 where 条件中的字段值
        :return:
        """
        upsets = []
        values = []
        for k, v in updates.items():
            s = f'`{k}`=?'
            upsets.append(s)
            values.append(v)
        upsets = ','.join(upsets)
        values.append(value_where)
        sql = f'UPDATE {table_name} SET {upsets} WHERE {field_where}=?'
        
        async with self._lock:
            async with aiosqlite.connect(self.__db_path) as conn:
                cursor = await conn.execute(sql, values)
                await conn.commit()
                return cursor.rowcount

    async def execute(self, sql: str, *args: Union[str, int]) -> int:
        """
        需要更新、写入等操作的 excute 执行语句
        :param sql:
        :param args:
        :return:
        """
        async with self._lock:
            async with aiosqlite.connect(self.__db_path) as conn:
                # 如果SQL包含多个语句，需要分别执行
                if ';' in sql and not args:
                    # 分割SQL语句并逐个执行
                    statements = [stmt.strip() for stmt in sql.split(';') if stmt.strip()]
                    total_rowcount = 0
                    for statement in statements:
                        cursor = await conn.execute(statement)
                        total_rowcount += cursor.rowcount
                    await conn.commit()
                    return total_rowcount
                else:
                    cursor = await conn.execute(sql, args)
                    await conn.commit()
                    return cursor.rowcount

    async def execute_many(self, sql: str, args_list: List[tuple]) -> int:
        """
        批量执行SQL语句
        :param sql: SQL语句
        :param args_list: 参数列表
        :return: 影响的行数
        """
        async with self._lock:
            async with aiosqlite.connect(self.__db_path) as conn:
                cursor = await conn.executemany(sql, args_list)
                await conn.commit()
                return cursor.rowcount

    async def close(self):
        """
        关闭数据库连接（SQLite不需要显式关闭连接池）
        """
        pass