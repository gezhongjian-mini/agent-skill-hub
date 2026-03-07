# Skill Template

## 描述
这是一个 Skill 模板，用于创建新的 Agent Skill。

## 作者
- 姓名: Your Name
- 邮箱: your.email@example.com
- 日期: 2024-03-07

## 功能
- 功能1: 描述功能1
- 功能2: 描述功能2
- 功能3: 描述功能3

## 使用方法

### 基本用法
```python
from src.main import MySkill

skill = MySkill()
result = skill.run("输入参数")
print(result)
```

### 高级用法
```python
# 高级配置示例
skill = MySkill(config={
    "option1": "value1",
    "option2": "value2"
})
```

## 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| param1 | string | 是 | 参数1说明 |
| param2 | int | 否 | 参数2说明，默认值为0 |

## 返回值

```json
{
  "status": "success",
  "data": {},
  "message": "操作成功"
}
```

## 依赖

- Python >= 3.8
- requests >= 2.28.0
- 其他依赖...

## 安装

```bash
pip install -r requirements.txt
```

## 测试

```bash
python -m pytest tests/
```

## 版本历史

- v1.0.0 (2024-03-07): 初始版本
- v1.1.0 (2024-03-08): 添加新功能

## 注意事项

1. 注意点1
2. 注意点2
3. 注意点3

## 参考链接

- [相关文档1](url1)
- [相关文档2](url2)
