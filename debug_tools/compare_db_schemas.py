#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库表结构对比工具
用于对比SQLite和MySQL数据库表结构的差异
"""

import re
import os
from typing import Dict, List, Set, Tuple, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ColumnInfo:
    """列信息"""
    name: str
    data_type: str
    nullable: bool = True
    default_value: str = None
    primary_key: bool = False
    auto_increment: bool = False
    comment: str = ""

    def __str__(self):
        return f"{self.name} {self.data_type}"


@dataclass
class IndexInfo:
    """索引信息"""
    name: str
    columns: List[str]
    unique: bool = False
    primary: bool = False

    def __str__(self):
        if self.primary:
            return f"PRIMARY KEY ({', '.join(self.columns)})"
        unique_str = "UNIQUE " if self.unique else ""
        return f"{unique_str}INDEX {self.name} ({', '.join(self.columns)})"


@dataclass
class TableInfo:
    """表信息"""
    name: str
    columns: Dict[str, ColumnInfo]
    indexes: Dict[str, IndexInfo]
    comment: str = ""


class SQLSchemaParser:
    """SQL表结构解析器"""
    
    def __init__(self, sql_file_path: str):
        self.sql_file_path = sql_file_path
        self.tables: Dict[str, TableInfo] = {}
        self.current_table_name = None
    
    def parse(self) -> Dict[str, TableInfo]:
        """解析SQL文件"""
        if not os.path.exists(self.sql_file_path):
            raise FileNotFoundError(f"SQL文件不存在: {self.sql_file_path}")
        
        with open(self.sql_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析CREATE TABLE语句
        self._parse_create_tables(content)
        
        # 解析CREATE INDEX语句
        self._parse_create_indexes(content)
        
        return self.tables
    
    def _parse_create_tables(self, content: str):
        """解析CREATE TABLE语句"""
        # 匹配CREATE TABLE语句的正则表达式
        table_pattern = r'CREATE TABLE `?([^`\s]+)`?\s*\((.*?)\)(?:\s*ENGINE=.*?)?(?:\s*COMMENT=.*?)?;'
        
        for match in re.finditer(table_pattern, content, re.DOTALL | re.IGNORECASE):
            table_name = match.group(1)
            table_body = match.group(2)
            

            
            # 解析表注释
            comment_match = re.search(r"COMMENT\s*=\s*['\"]([^'\"]*)['\"]?", match.group(0), re.IGNORECASE)
            table_comment = comment_match.group(1) if comment_match else ""
            
            # 设置当前表名，用于索引解析
            self.current_table_name = table_name
            
            # 先创建表信息对象
            self.tables[table_name] = TableInfo(
                name=table_name,
                columns={},
                indexes={},
                comment=table_comment
            )
            
            # 解析列定义
            columns = self._parse_columns(table_body)
            self.tables[table_name].columns = columns
            

    
    def _parse_columns(self, table_body: str) -> Dict[str, ColumnInfo]:
        """解析列定义"""
        columns = {}
        
        # 更智能的分割方式：按行分割，然后重新组合
        lines = [line.strip() for line in table_body.split('\n') if line.strip()]
        
        # 重新组合成完整的定义项
        items = []
        current_item = ""
        paren_count = 0
        
        for line in lines:
            current_item += line + " "
            paren_count += line.count('(') - line.count(')')
            
            # 如果括号平衡且以逗号结尾，或者是最后一行
            if paren_count == 0 and (line.rstrip().endswith(',') or line == lines[-1]):
                items.append(current_item.strip().rstrip(','))
                current_item = ""
        
        # 如果还有剩余内容
        if current_item.strip():
            items.append(current_item.strip().rstrip(','))
        
        # 解析每个项目
        for item in items:
            item = item.strip()
            if not item:
                continue
                
            # 检查是否是索引定义
            if re.match(r'^(PRIMARY\s+KEY|KEY|INDEX|UNIQUE)', item, re.IGNORECASE):
                self._parse_table_index(item)
            else:
                # 尝试解析为列定义
                column_info = self._parse_single_column(item)
                if column_info:
                    columns[column_info.name] = column_info
        
        return columns
    
    def _parse_table_index(self, index_def: str):
        """解析表内索引定义"""
        index_def = index_def.strip()
        
        if not hasattr(self, 'current_table_name') or not self.current_table_name:
            return
        
        # 解析PRIMARY KEY
        if re.match(r'^PRIMARY\s+KEY', index_def, re.IGNORECASE):
            columns_match = re.search(r'\(([^)]+)\)', index_def)
            if columns_match:
                columns = [col.strip().strip('`') for col in columns_match.group(1).split(',')]
                if self.current_table_name in self.tables:
                    self.tables[self.current_table_name].indexes['PRIMARY'] = IndexInfo(
                        name='PRIMARY',
                        columns=columns,
                        unique=True,
                        primary=True
                    )

        
        # 解析普通索引和唯一索引
        elif re.match(r'^(UNIQUE\s+)?(KEY|INDEX)', index_def, re.IGNORECASE):
            unique = 'UNIQUE' in index_def.upper()
            
            # 提取索引名和列，支持MySQL的KEY语法
            # 匹配格式: KEY `index_name` (`column1`, `column2`)
            pattern = r'(?:UNIQUE\s+)?(?:KEY|INDEX)\s+`?([^`\s]+)`?\s*\(([^)]+)\)'
            match = re.search(pattern, index_def, re.IGNORECASE)
            
            if match:
                index_name = match.group(1)
                columns_str = match.group(2)
                # 解析列名，去除反引号和空格
                columns = [col.strip().strip('`').strip() for col in columns_str.split(',')]
                
                if self.current_table_name in self.tables:
                    self.tables[self.current_table_name].indexes[index_name] = IndexInfo(
                        name=index_name,
                        columns=columns,
                        unique=unique
                    )

    
    def _is_complete_column_definition(self, definition: str) -> bool:
        """检查是否是完整的列定义"""
        # 简单检查：如果包含数据类型关键字，认为是完整的
        type_keywords = ['INTEGER', 'TEXT', 'VARCHAR', 'INT', 'BIGINT', 'LONGTEXT', 'DATETIME']
        return any(keyword in definition.upper() for keyword in type_keywords)
    
    def _parse_single_column(self, column_def: str) -> ColumnInfo:
        """解析单个列定义"""
        column_def = column_def.strip()
        
        # 提取列名（去除反引号）
        name_match = re.match(r'`?([^`\s]+)`?', column_def)
        if not name_match:
            return None
        
        column_name = name_match.group(1)
        
        # 提取数据类型
        type_pattern = r'`?[^`\s]+`?\s+([^\s]+(?:\([^)]+\))?)'  
        type_match = re.search(type_pattern, column_def)
        data_type = type_match.group(1) if type_match else "UNKNOWN"
        
        # 检查各种属性
        nullable = 'NOT NULL' not in column_def.upper()
        primary_key = 'PRIMARY KEY' in column_def.upper()
        auto_increment = 'AUTO_INCREMENT' in column_def.upper() or 'AUTOINCREMENT' in column_def.upper()
        
        # 提取默认值
        default_match = re.search(r"DEFAULT\s+([^\s,]+|'[^']*'|\"[^\"]*\")", column_def, re.IGNORECASE)
        default_value = default_match.group(1) if default_match else None
        
        # 提取注释
        comment_match = re.search(r"COMMENT\s+['\"]([^'\"]*)['\"]?", column_def, re.IGNORECASE)
        comment = comment_match.group(1) if comment_match else ""
        
        return ColumnInfo(
            name=column_name,
            data_type=data_type,
            nullable=nullable,
            default_value=default_value,
            primary_key=primary_key,
            auto_increment=auto_increment,
            comment=comment
        )
    
    def _parse_create_indexes(self, content: str):
        """解析CREATE INDEX语句"""
        # 匹配CREATE INDEX语句
        index_pattern = r'CREATE\s+(UNIQUE\s+)?INDEX\s+`?([^`\s]+)`?\s+ON\s+`?([^`\s]+)`?\s*\(([^)]+)\)'
        
        for match in re.finditer(index_pattern, content, re.IGNORECASE):
            unique = bool(match.group(1))
            index_name = match.group(2)
            table_name = match.group(3)
            columns_str = match.group(4)
            
            # 解析列名
            columns = [col.strip().strip('`') for col in columns_str.split(',')]
            
            if table_name in self.tables:
                self.tables[table_name].indexes[index_name] = IndexInfo(
                    name=index_name,
                    columns=columns,
                    unique=unique
                )


class DatabaseSchemaComparator:
    """数据库表结构对比器"""
    
    def __init__(self, sqlite_sql_path: str, mysql_sql_path: str):
        self.sqlite_sql_path = sqlite_sql_path
        self.mysql_sql_path = mysql_sql_path
        self.sqlite_tables = {}
        self.mysql_tables = {}
    
    def compare(self):
        """执行对比"""
        print("开始解析数据库表结构...")
        
        # 解析SQLite表结构
        print(f"解析SQLite表结构: {self.sqlite_sql_path}")
        sqlite_parser = SQLSchemaParser(self.sqlite_sql_path)
        self.sqlite_tables = sqlite_parser.parse()
        print(f"SQLite解析完成，发现 {len(self.sqlite_tables)} 个表")
        
        # 解析MySQL表结构
        print(f"解析MySQL表结构: {self.mysql_sql_path}")
        mysql_parser = SQLSchemaParser(self.mysql_sql_path)
        self.mysql_tables = mysql_parser.parse()
        print(f"MySQL解析完成，发现 {len(self.mysql_tables)} 个表")
        
        print("\n" + "="*80)
        print("数据库表结构对比报告")
        print("="*80)
        
        # 对比表
        self._compare_tables()
        
        # 对比每个表的结构
        common_tables = set(self.sqlite_tables.keys()) & set(self.mysql_tables.keys())
        for table_name in sorted(common_tables):
            self._compare_table_structure(table_name)
    
    def _compare_tables(self):
        """对比表列表"""
        sqlite_table_names = set(self.sqlite_tables.keys())
        mysql_table_names = set(self.mysql_tables.keys())
        
        common_tables = sqlite_table_names & mysql_table_names
        sqlite_only = sqlite_table_names - mysql_table_names
        mysql_only = mysql_table_names - sqlite_table_names
        
        print(f"\n表数量对比:")
        print(f"   SQLite表数量: {len(sqlite_table_names)}")
        print(f"   MySQL表数量: {len(mysql_table_names)}")
        print(f"   共同表数量: {len(common_tables)}")
        
        if sqlite_only:
            print(f"\n仅存在于SQLite的表 ({len(sqlite_only)}个):")
            for table in sorted(sqlite_only):
                print(f"   - {table}")
        
        if mysql_only:
            print(f"\n仅存在于MySQL的表 ({len(mysql_only)}个):")
            for table in sorted(mysql_only):
                print(f"   - {table}")
        
        if not sqlite_only and not mysql_only:
            print("两个数据库的表列表完全一致")
    
    def _compare_table_structure(self, table_name: str):
        """对比单个表的结构"""
        sqlite_table = self.sqlite_tables[table_name]
        mysql_table = self.mysql_tables[table_name]
        
        print(f"\n表 '{table_name}' 结构对比:")
        
        # 对比列
        self._compare_columns(table_name, sqlite_table.columns, mysql_table.columns)
        
        # 对比索引
        self._compare_indexes(table_name, sqlite_table.indexes, mysql_table.indexes)
    
    def _compare_columns(self, table_name: str, sqlite_columns: Dict[str, ColumnInfo], mysql_columns: Dict[str, ColumnInfo]):
        """对比列结构"""
        sqlite_col_names = set(sqlite_columns.keys())
        mysql_col_names = set(mysql_columns.keys())
        
        common_columns = sqlite_col_names & mysql_col_names
        sqlite_only = sqlite_col_names - mysql_col_names
        mysql_only = mysql_col_names - sqlite_col_names
        
        # 检查列差异
        if sqlite_only:
            print(f"   仅存在于SQLite的列:")
            for col in sorted(sqlite_only):
                col_info = sqlite_columns[col]
                print(f"      - {col_info.name}: {col_info.data_type}")
        
        if mysql_only:
            print(f"   仅存在于MySQL的列:")
            for col in sorted(mysql_only):
                col_info = mysql_columns[col]
                print(f"      - {col_info.name}: {col_info.data_type}")
        
        # 检查共同列的差异
        column_differences = []
        for col_name in sorted(common_columns):
            sqlite_col = sqlite_columns[col_name]
            mysql_col = mysql_columns[col_name]
            
            differences = []
            
            # 对比数据类型（简化对比，忽略大小写和一些等价类型）
            if not self._are_types_equivalent(sqlite_col.data_type, mysql_col.data_type):
                differences.append(f"类型: SQLite({sqlite_col.data_type}) vs MySQL({mysql_col.data_type})")
            
            # 对比可空性
            if sqlite_col.nullable != mysql_col.nullable:
                differences.append(f"可空性: SQLite({'NULL' if sqlite_col.nullable else 'NOT NULL'}) vs MySQL({'NULL' if mysql_col.nullable else 'NOT NULL'})")
            
            # 对比默认值
            if sqlite_col.default_value != mysql_col.default_value:
                differences.append(f"默认值: SQLite({sqlite_col.default_value}) vs MySQL({mysql_col.default_value})")
            
            if differences:
                column_differences.append((col_name, differences))
        
        if column_differences:
            print(f"   列定义差异:")
            for col_name, diffs in column_differences:
                print(f"      - {col_name}:")
                for diff in diffs:
                    print(f"        * {diff}")
        
        if not sqlite_only and not mysql_only and not column_differences:
            print(f"   列结构完全一致 ({len(common_columns)}个列)")
    
    def _are_types_equivalent(self, sqlite_type: str, mysql_type: str) -> bool:
        """检查两种数据类型是否等价"""
        # 标准化类型名称
        sqlite_type = sqlite_type.upper().strip()
        mysql_type = mysql_type.upper().strip()
        
        # 直接相等
        if sqlite_type == mysql_type:
            return True
        
        # 等价类型映射
        equivalents = {
            'INTEGER': ['INT', 'BIGINT'],
            'TEXT': ['VARCHAR', 'LONGTEXT'],
            'REAL': ['FLOAT', 'DOUBLE'],
            'BLOB': ['LONGBLOB']
        }
        
        # 检查是否为等价类型
        for sqlite_base, mysql_equivalents in equivalents.items():
            if sqlite_type.startswith(sqlite_base):
                for mysql_equiv in mysql_equivalents:
                    if mysql_type.startswith(mysql_equiv):
                        return True
        
        # 反向检查
        for sqlite_base, mysql_equivalents in equivalents.items():
            for mysql_equiv in mysql_equivalents:
                if mysql_type.startswith(mysql_equiv) and sqlite_type.startswith(sqlite_base):
                    return True
        
        return False
    
    def _compare_indexes(self, table_name: str, sqlite_indexes: Dict[str, IndexInfo], mysql_indexes: Dict[str, IndexInfo]):
        """对比索引结构"""
        sqlite_index_names = set(sqlite_indexes.keys())
        mysql_index_names = set(mysql_indexes.keys())
        
        # 过滤掉自动生成的索引
        sqlite_index_names = {name for name in sqlite_index_names if not name.startswith('sqlite_autoindex')}
        
        common_indexes = sqlite_index_names & mysql_index_names
        sqlite_only = sqlite_index_names - mysql_index_names
        mysql_only = mysql_index_names - sqlite_index_names
        
        if sqlite_only:
            print(f"   仅存在于SQLite的索引:")
            for idx in sorted(sqlite_only):
                idx_info = sqlite_indexes[idx]
                print(f"      - {idx_info}")
        
        if mysql_only:
            print(f"   仅存在于MySQL的索引:")
            for idx in sorted(mysql_only):
                idx_info = mysql_indexes[idx]
                print(f"      - {idx_info}")
        
        # 检查共同索引的差异
        index_differences = []
        for idx_name in sorted(common_indexes):
            sqlite_idx = sqlite_indexes[idx_name]
            mysql_idx = mysql_indexes[idx_name]
            
            differences = []
            
            if sqlite_idx.columns != mysql_idx.columns:
                differences.append(f"列: SQLite({sqlite_idx.columns}) vs MySQL({mysql_idx.columns})")
            
            if sqlite_idx.unique != mysql_idx.unique:
                differences.append(f"唯一性: SQLite({sqlite_idx.unique}) vs MySQL({mysql_idx.unique})")
            
            if differences:
                index_differences.append((idx_name, differences))
        
        if index_differences:
            print(f"   索引定义差异:")
            for idx_name, diffs in index_differences:
                print(f"      - {idx_name}:")
                for diff in diffs:
                    print(f"        * {diff}")
        
        if not sqlite_only and not mysql_only and not index_differences:
            print(f"   索引结构完全一致 ({len(common_indexes)}个索引)")


def main():
    """主函数"""
    # 获取脚本所在目录的上级目录（项目根目录）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # 构建SQL文件路径
    sqlite_sql_path = os.path.join(project_root, "schema", "sqlite_tables.sql")
    mysql_sql_path = os.path.join(project_root, "schema", "mysql_tables.sql")
    
    print("数据库表结构对比工具")
    print(f"SQLite表结构文件: {sqlite_sql_path}")
    print(f"MySQL表结构文件: {mysql_sql_path}")
    print(f"对比时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 检查文件是否存在
        if not os.path.exists(sqlite_sql_path):
            print(f"SQLite表结构文件不存在: {sqlite_sql_path}")
            return
        
        if not os.path.exists(mysql_sql_path):
            print(f"MySQL表结构文件不存在: {mysql_sql_path}")
            return
        
        # 执行对比
        comparator = DatabaseSchemaComparator(sqlite_sql_path, mysql_sql_path)
        comparator.compare()
        
        print("\n" + "="*80)
        print("对比完成！")
        print("="*80)
        
    except Exception as e:
        print(f"对比过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()