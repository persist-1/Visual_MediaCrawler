#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库分析工具
用于分析SQLite数据库结构并导出为SQL文件和数据模型文件
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any, Tuple
import json


class SQLiteAnalyzer:
    """SQLite数据库分析器"""
    
    def __init__(self, db_path: str):
        """
        初始化分析器
        
        Args:
            db_path: SQLite数据库文件路径
        """
        self.db_path = db_path
        self.conn = None
        
    def connect(self):
        """连接数据库"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            print(f"✅ 成功连接到数据库: {self.db_path}")
        except Exception as e:
            print(f"❌ 连接数据库失败: {e}")
            raise
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            print("✅ 数据库连接已关闭")
    
    def get_all_tables(self) -> List[str]:
        """获取所有表名"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📊 发现 {len(tables)} 个数据表")
        return tables
    
    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """获取表结构信息"""
        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = []
        for row in cursor.fetchall():
            columns.append({
                'cid': row[0],
                'name': row[1],
                'type': row[2],
                'notnull': bool(row[3]),
                'default_value': row[4],
                'pk': bool(row[5])
            })
        return columns
    
    def get_table_indexes(self, table_name: str) -> List[Dict[str, Any]]:
        """获取表索引信息"""
        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA index_list({table_name})")
        indexes = []
        for row in cursor.fetchall():
            index_name = row[1]
            # 获取索引详细信息
            cursor.execute(f"PRAGMA index_info({index_name})")
            index_columns = [col[2] for col in cursor.fetchall()]
            indexes.append({
                'name': index_name,
                'unique': bool(row[2]),
                'columns': index_columns
            })
        return indexes
    
    def get_table_create_sql(self, table_name: str) -> str:
        """获取表的创建SQL语句"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT sql FROM sqlite_master 
            WHERE type='table' AND name=?
        """, (table_name,))
        result = cursor.fetchone()
        return result[0] if result else ""
    
    def _enhance_create_sql(self, original_sql: str, columns: List[Dict[str, Any]]) -> str:
        """增强CREATE TABLE语句，确保包含task_times_id字段"""
        # 检查是否已有task_times_id字段
        has_task_times_id = any(col['name'] == 'task_times_id' for col in columns)
        
        if has_task_times_id:
            return original_sql
        
        # 如果没有task_times_id字段，添加它
        # 找到最后一个字段的位置
        if original_sql.endswith(');'):
            # 在最后一个字段后添加task_times_id
            enhanced_sql = original_sql[:-2] + ',\n    `task_times_id` TEXT DEFAULT NULL\n);'
            return enhanced_sql
        elif original_sql.endswith(')'):
            enhanced_sql = original_sql[:-1] + ',\n    `task_times_id` TEXT DEFAULT NULL\n)'
            return enhanced_sql
        else:
            return original_sql
    
    def get_table_row_count(self, table_name: str) -> int:
        """获取表的行数"""
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        return cursor.fetchone()[0]
    
    def analyze_database(self) -> Dict[str, Any]:
        """分析整个数据库"""
        print("🔍 开始分析数据库...")
        
        analysis = {
            'database_path': self.db_path,
            'analysis_time': datetime.now().isoformat(),
            'tables': {}
        }
        
        tables = self.get_all_tables()
        
        for table_name in tables:
            print(f"📋 分析表: {table_name}")
            
            columns = self.get_table_info(table_name)
            indexes = self.get_table_indexes(table_name)
            create_sql = self.get_table_create_sql(table_name)
            row_count = self.get_table_row_count(table_name)
            
            # 检查并添加task_times_id字段信息
            enhanced_columns = self._ensure_task_times_id_column(columns)
            
            analysis['tables'][table_name] = {
                'columns': enhanced_columns,
                'indexes': indexes,
                'create_sql': create_sql,
                'row_count': row_count
            }
        
        print(f"✅ 数据库分析完成，共分析 {len(tables)} 个表")
        return analysis
    
    def export_to_sql(self, output_path: str, analysis: Dict[str, Any]):
        """导出为SQL文件"""
        print(f"📝 导出SQL文件到: {output_path}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"-- SQLite数据库结构导出\n")
            f.write(f"-- 数据库文件: {analysis['database_path']}\n")
            f.write(f"-- 导出时间: {analysis['analysis_time']}\n")
            f.write(f"-- 生成工具: MediaCrawler DB Analyzer\n\n")
            
            for table_name, table_info in analysis['tables'].items():
                f.write(f"-- ----------------------------\n")
                f.write(f"-- Table structure for {table_name}\n")
                f.write(f"-- ----------------------------\n")
                f.write(f"DROP TABLE IF EXISTS `{table_name}`;\n")
                
                # 重新构建CREATE TABLE语句，确保包含task_times_id字段
                enhanced_sql = self._enhance_create_sql(table_info['create_sql'], table_info['columns'])
                f.write(f"{enhanced_sql};\n\n")
                
                # 生成实际的CREATE INDEX语句
                if table_info['indexes']:
                    for index in table_info['indexes']:
                        if not index['name'].startswith('sqlite_autoindex'):
                            columns_str = '`, `'.join(index['columns'])
                            if index['unique']:
                                f.write(f"CREATE UNIQUE INDEX `{index['name']}` ON `{table_name}` (`{columns_str}`);\n")
                            else:
                                f.write(f"CREATE INDEX `{index['name']}` ON `{table_name}` (`{columns_str}`);\n")
                    
                    # 为task_times_id字段添加索引（如果存在且没有索引）
                    has_task_times_id = any(col['name'] == 'task_times_id' for col in table_info['columns'])
                    has_task_times_id_index = any('task_times_id' in index['columns'] for index in table_info['indexes'])
                    
                    if has_task_times_id and not has_task_times_id_index:
                        f.write(f"CREATE INDEX `idx_{table_name}_task_times_id` ON `{table_name}` (`task_times_id`);\n")
                    
                    f.write("\n")
        
        print("✅ SQL文件导出完成")
    
    def export_to_datamodel(self, output_path: str, analysis: Dict[str, Any]):
        """导出为Python数据模型文件"""
        print(f"🐍 导出数据模型文件到: {output_path}")
        
        # SQLite到Python类型映射
        type_mapping = {
            'INTEGER': 'int',
            'TEXT': 'str',
            'REAL': 'float',
            'BLOB': 'bytes',
            'NUMERIC': 'float',
            'VARCHAR': 'str',
            'CHAR': 'str',
            'DATETIME': 'datetime',
            'TIMESTAMP': 'datetime',
            'DATE': 'date',
            'TIME': 'time',
            'BOOLEAN': 'bool',
            'BOOL': 'bool'
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('#!/usr/bin/env python3\n')
            f.write('# -*- coding: utf-8 -*-\n')
            f.write('"""\n')
            f.write('数据模型定义\n')
            f.write(f'从SQLite数据库自动生成: {analysis["database_path"]}\n')
            f.write(f'生成时间: {analysis["analysis_time"]}\n')
            f.write('生成工具: MediaCrawler DB Analyzer\n')
            f.write('"""\n\n')
            
            f.write('from datetime import datetime, date, time\n')
            f.write('from typing import Optional, List\n')
            f.write('from dataclasses import dataclass\n')
            f.write('from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float\n')
            f.write('from sqlalchemy.ext.declarative import declarative_base\n\n')
            
            f.write('Base = declarative_base()\n\n')
            
            # 生成数据类
            for table_name, table_info in analysis['tables'].items():
                class_name = self._table_name_to_class_name(table_name)
                
                f.write(f'@dataclass\n')
                f.write(f'class {class_name}Data:\n')
                f.write(f'    """数据类: {table_name} (行数: {table_info["row_count"]})"""\n')
                
                for col in table_info['columns']:
                    python_type = self._sqlite_type_to_python(col['type'], type_mapping)
                    optional = '' if col['notnull'] or col['pk'] else 'Optional['
                    optional_end = '' if col['notnull'] or col['pk'] else ']'
                    default = ' = None' if not col['notnull'] and not col['pk'] else ''
                    
                    f.write(f'    {col["name"]}: {optional}{python_type}{optional_end}{default}\n')
                
                f.write('\n')
                
                # 生成SQLAlchemy模型
                f.write(f'class {class_name}(Base):\n')
                f.write(f'    """SQLAlchemy模型: {table_name}"""\n')
                f.write(f'    __tablename__ = \'{table_name}\'\n\n')
                
                for col in table_info['columns']:
                    sqlalchemy_type = self._sqlite_type_to_sqlalchemy(col['type'])
                    primary_key = ', primary_key=True' if col['pk'] else ''
                    nullable = ', nullable=False' if col['notnull'] else ''
                    
                    f.write(f'    {col["name"]} = Column({sqlalchemy_type}{primary_key}{nullable})\n')
                
                f.write('\n')
                
                # 添加索引信息作为注释
                if table_info['indexes']:
                    f.write(f'    # 索引信息:\n')
                    for index in table_info['indexes']:
                        if not index['name'].startswith('sqlite_autoindex'):
                            index_type = 'UNIQUE' if index['unique'] else 'INDEX'
                            f.write(f'    # - {index["name"]}: {", ".join(index["columns"])} ({index_type})\n')
                
                f.write('\n\n')
        
        print("✅ 数据模型文件导出完成")
    
    def _table_name_to_class_name(self, table_name: str) -> str:
        """将表名转换为类名"""
        # 移除前缀，转换为驼峰命名
        parts = table_name.split('_')
        return ''.join(word.capitalize() for word in parts)
    
    def _sqlite_type_to_python(self, sqlite_type: str, type_mapping: Dict[str, str]) -> str:
        """将SQLite类型转换为Python类型"""
        sqlite_type = sqlite_type.upper()
        for sql_type, py_type in type_mapping.items():
            if sql_type in sqlite_type:
                return py_type
        return 'str'  # 默认类型
    
    def _sqlite_type_to_sqlalchemy(self, sqlite_type: str) -> str:
        """将SQLite类型转换为SQLAlchemy类型"""
        sqlite_type = sqlite_type.upper()
        if 'INTEGER' in sqlite_type:
            return 'Integer'
        elif 'TEXT' in sqlite_type or 'VARCHAR' in sqlite_type or 'CHAR' in sqlite_type:
            return 'Text'
        elif 'REAL' in sqlite_type or 'FLOAT' in sqlite_type or 'NUMERIC' in sqlite_type:
            return 'Float'
        elif 'DATETIME' in sqlite_type or 'TIMESTAMP' in sqlite_type:
            return 'DateTime'
        elif 'BOOL' in sqlite_type:
            return 'Boolean'
        else:
            return 'String'
    
    def _ensure_task_times_id_column(self, columns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """确保列信息中包含task_times_id字段"""
        # 检查是否已有task_times_id字段
        has_task_times_id = any(col['name'] == 'task_times_id' for col in columns)
        
        if not has_task_times_id:
            # 添加task_times_id字段
            task_times_id_col = {
                'cid': len(columns),
                'name': 'task_times_id',
                'type': 'TEXT',
                'notnull': False,
                'default_value': None,
                'pk': False
            }
            columns.append(task_times_id_col)
        
        return columns
    
    def export_analysis_json(self, output_path: str, analysis: Dict[str, Any]):
        """导出分析结果为JSON文件"""
        print(f"📄 导出分析结果到: {output_path}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
        
        print("✅ JSON文件导出完成")


def main():
    """主函数"""
    # 数据库路径
    db_path = "d:/A_work/A_trae_alter/MediaCrawler-main/data/mc.db"
    
    # 输出目录
    output_dir = "./output"
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建分析器
    analyzer = SQLiteAnalyzer(db_path)
    
    try:
        # 连接数据库
        analyzer.connect()
        
        # 分析数据库
        analysis = analyzer.analyze_database()
        
        # 生成时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 导出文件
        sql_file = os.path.join(output_dir, f"database_structure_{timestamp}.sql")
        model_file = os.path.join(output_dir, f"datamodel_{timestamp}.py")
        json_file = os.path.join(output_dir, f"analysis_{timestamp}.json")
        
        analyzer.export_to_sql(sql_file, analysis)
        analyzer.export_to_datamodel(model_file, analysis)
        analyzer.export_analysis_json(json_file, analysis)
        
        print("\n🎉 所有文件导出完成!")
        print(f"📁 输出目录: {os.path.abspath(output_dir)}")
        print(f"📄 SQL文件: {sql_file}")
        print(f"🐍 数据模型: {model_file}")
        print(f"📊 分析结果: {json_file}")
        
    except Exception as e:
        print(f"❌ 执行失败: {e}")
    finally:
        analyzer.close()


if __name__ == "__main__":
    main()