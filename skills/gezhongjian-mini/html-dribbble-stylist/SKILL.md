# HTML Dribbble Stylist Skill

## 描述
创建具有 Dribbble 风格设计的精美 HTML 页面，包含现代 UI、动画和视觉效果。从 Dribbble 热门设计中获取灵感，应用专业样式和微妙动画。

## 作者
- 姓名: gezhongjian-mini
- 日期: 2026-03-07

## 功能
- **获取设计灵感**: 从 Dribbble 热门作品浏览当前设计趋势
- **提取设计元素**: 色彩、卡片样式、排版、布局
- **应用动画效果**: 淡入、悬停提升、进度条动画
- **生成完整 HTML**: 自包含的响应式页面

## 使用方法

### 命令行
```bash
python src/skill.py create "产品展示页面" --type landing
```

### Python API
```python
from src.skill import DribbbleStylist

stylist = DribbbleStylist()
html = stylist.create_page(
    title="产品展示",
    content=data,
    style="card-layout"
)
```

## 设计原则
- **简洁背景**: 浅灰色或微妙渐变
- **卡片布局**: 白色卡片、柔和阴影、12-20px 圆角
- **状态颜色**: 绿(成功)、蓝(活跃)、橙(警告)、紫(完成)
- **渐进展示**: 卡片依次动画进入
- **微交互**: 悬停状态、平滑过渡

## 依赖
- Python >= 3.8
- requests >= 2.28.0

## 版本历史
- v1.0.0 (2026-03-07): 初始版本
