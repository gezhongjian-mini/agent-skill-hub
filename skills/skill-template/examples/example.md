# 示例 Skill

## 基本用法

```python
from src.main import MySkill

# 创建实例
skill = MySkill()

# 执行
result = skill.run("输入参数")
print(result)
```

## 高级配置

```python
# 带配置
skill = MySkill(config={
    "timeout": 30,
    "retries": 3
})

# 批量处理
inputs = ["input1", "input2", "input3"]
results = [skill.run(i) for i in inputs]
```

## 命令行使用

```bash
python src/main.py --input "参数" --config config.json
```
