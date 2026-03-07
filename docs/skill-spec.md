# Skill 规范

## 目录结构

```
skill-name/
├── SKILL.md              # 必需: Skill 文档
├── metadata.json         # 必需: 元数据
├── src/                  # 必需: 源代码
│   └── main.py          # 主入口
├── examples/            # 推荐: 使用示例
│   └── example.md
├── tests/               # 推荐: 测试
│   └── test_skill.py
└── requirements.txt     # 可选: 依赖
```

## metadata.json 格式

```json
{
  "name": "skill-name",
  "version": "1.0.0",
  "author": "your-name",
  "description": "简短描述",
  "tags": ["api", "weather"],
  "language": "python",
  "dependencies": ["requests>=2.28.0"],
  "entryPoint": "src/main.py",
  "created": "2024-03-07T00:00:00Z",
  "updated": "2024-03-07T00:00:00Z"
}
```

## SKILL.md 章节

必需章节:
1. 描述
2. 作者
3. 功能
4. 使用方法
5. 版本历史

可选章节:
- 参数说明
- 返回值
- 依赖
- 安装
- 测试
- 注意事项
- 参考链接

## 代码规范

### Python

```python
from typing import Dict, Any

class MySkill:
    """Skill 描述"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
    
    def run(self, input_data: str) -> Dict[str, Any]:
        """
        执行 skill
        
        Args:
            input_data: 输入数据
            
        Returns:
            结果字典
        """
        # 实现
        return {"status": "success", "data": {}}
```

## 版本号规范

使用语义化版本: `MAJOR.MINOR.PATCH`

- MAJOR: 不兼容的 API 更改
- MINOR: 向后兼容的功能添加
- PATCH: 向后兼容的问题修复
