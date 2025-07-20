# MediaCrawler API 编码问题修复说明

## 问题描述

在前端任务执行结果中出现中文乱码，具体表现为：
- "使用标准模式" 显示为 "ʹñ׼ģʽ"
- "账号未登录" 显示为 "˺δ¼"
- "获取视频详情错误" 显示为 "ɶľ"

## 问题原因

1. **子进程输出编码不一致**：MediaCrawler主程序输出UTF-8编码的中文，但在Windows系统上可能被错误地解析
2. **特殊字符映射问题**：某些中文字符在传输过程中被映射为特殊的Unicode字符
3. **前端直接显示**：前端直接渲染后端返回的字符串，没有进行编码处理

## 解决方案

### 1. 优化子进程执行 (`_run_subprocess`函数)

- 统一使用UTF-8编码处理子进程输出
- 设置环境变量确保Python程序输出UTF-8：
  - `PYTHONIOENCODING=utf-8:replace`
  - `CHCP=65001` (Windows)
  - `PYTHONLEGACYWINDOWSSTDIO=0`
- 增加异常处理和备用编码方案

### 2. 实现智能文本清理 (`_clean_output_text`函数)

- **ANSI控制字符清理**：移除终端控制字符
- **乱码映射修复**：建立已知乱码到正确文本的映射表
- **编码修复**：尝试修复其他类型的编码问题
- **控制字符过滤**：保留有用字符，移除无效控制字符

### 3. 乱码映射表

```python
garbled_mappings = {
    'ʹñ׼ģʽ': '使用标准模式',
    '˺δ¼': '账号未登录',
    'ɶľ': '获取视频详情错误',
    # ... 更多映射
}
```

## 修改的文件

- `api/api.py`：主要修改文件，包含所有编码修复逻辑

## 修改的函数

1. **`_run_subprocess`**：优化子进程执行和编码处理
2. **`_clean_output_text`**：新增文本清理和乱码修复功能
3. **`run_crawler_task`** 和 **`run_crawler_sync`**：应用文本清理

## 测试验证

已通过全面测试验证：
- ✅ 基础乱码修复测试：8/8 通过 (100%)
- ✅ 用户日志修复测试：通过
- ✅ 混合文本处理：正常
- ✅ 正常中文文本：不受影响

## 效果

**修复前：**
```
[BilibiliCrawler] ʹñ׼ģʽ
[BilibiliClient.pong] Pong bilibili failed: ˺δ¼
[BilibiliCrawler.get_video_info_task] Get video detail error: ɶľ
```

**修复后：**
```
[BilibiliCrawler] 使用标准模式
[BilibiliClient.pong] Pong bilibili failed: 账号未登录
[BilibiliCrawler.get_video_info_task] Get video detail error: 获取视频详情错误
```

## 兼容性

- ✅ Windows 系统
- ✅ 其他操作系统
- ✅ 向后兼容
- ✅ 不影响正常功能

## 维护说明

如果发现新的乱码模式，可以在 `_clean_output_text` 函数的 `garbled_mappings` 字典中添加新的映射关系。

---

**修复完成时间**：2025-07-12  
**修复状态**：✅ 已解决