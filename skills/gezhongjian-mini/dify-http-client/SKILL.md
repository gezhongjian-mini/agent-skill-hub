# Dify HTTP Client Skill

## 描述
综合 Dify Workflow 和 Chat 两种调用方式的 OpenClaw Skill。支持实时/异步 Workflow 执行和 SQL 查询。

## 作者
- 姓名: gezhongjian-mini
- 日期: 2026-03-07

## 功能
- **Workflow 实时模式**: 立即返回结果（~1秒）
- **Workflow 异步模式**: 提交任务返回ID，支持轮询（~5分钟）
- **Workflow 查询**: 查询异步任务执行结果
- **Chat SQL**: SQL助手，执行SQL并返回格式化结果
- **Chat 通用对话**: 支持任意文本查询

## 使用方法

### 命令行
```bash
# Workflow 实时模式
python src/skill.py dify_workflow_realtime

# Workflow 异步模式
python src/skill.py dify_workflow_async

# 查询异步任务
python src/skill.py dify_workflow_query <workflow_run_id>

# SQL 查询
python src/skill.py dify_chat_sql "select 1+2"

# 通用对话
python src/skill.py dify_chat "你好"
```

### Python API
```python
from src.skill import DifyAssistant

assistant = DifyAssistant(api_key="your-api-key")

# Workflow 实时
result = assistant.workflow_run("实时")

# Workflow 异步 + 轮询
result = assistant.workflow_run_and_wait("异步")

# SQL 查询
result = assistant.chat_sql("SELECT * FROM table")
```

## 配置
- **Base URL**: `http://dify-beta.panshi-gy.netease.com/v1`
- **Workflow API Key**: `app-1QqjBYvVZrvEqRREoN8vL64n`
- **Chat API Key**: `app-OuRmNS25dU8wUN0t0TFpTRq9`

## 依赖
- Python >= 3.8
- requests >= 2.28.0

## 版本历史
- v1.0.0 (2026-03-07): 初始版本，整合 Workflow 和 Chat 模式
