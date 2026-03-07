## 使用示例

### 示例 1: 创建简单页面
```bash
python src/skill.py create "产品展示"
```

### 示例 2: 指定输出文件
```bash
python src/skill.py create "数据分析看板" dashboard.html
```

### 示例 3: Python API
```python
from src.skill import DribbbleStylist

stylist = DribbbleStylist()
html = stylist.create_page(
    title="我的页面",
    content={"items": []},
    style="card-layout"
)

# 保存到文件
stylist.save_page(html, "my-page.html")
```
