## 使用示例

### 示例 1: Workflow 实时模式
```bash
python src/skill.py dify_workflow_realtime
```

### 示例 2: Workflow 异步模式 + 轮询
```bash
# 提交任务
python src/skill.py dify_workflow_async

# 查询结果
python src/skill.py dify_workflow_query <workflow_run_id>
```

### 示例 3: SQL 查询
```bash
python src/skill.py dify_chat_sql "SELECT COUNT(*) FROM users"
```

### 示例 4: Python 代码
```python
from src.skill import DifyAssistant

assistant = DifyAssistant()
result = assistant.workflow_run_and_wait("异步", poll_interval=30)
print(result["outputs"])
```
