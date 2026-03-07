# Skills 目录

此目录存放所有 Agent Skill。

## 目录结构

```
skills/
├── skill-template/          # Skill 模板
│   ├── SKILL.md
│   ├── metadata.json
│   ├── src/
│   ├── examples/
│   └── tests/
└── [author-name]/           # 作者目录
    └── [skill-name]/        # Skill 目录
```

## 添加新 Skill

1. 创建作者目录: `mkdir skills/your-name`
2. 复制模板: `cp -r skills/skill-template skills/your-name/my-skill`
3. 编辑文件
4. 验证: `python scripts/validate-skill.py skills/your-name/my-skill`
5. 更新注册表: `python scripts/update-registry.py`

## 命名规范

- 作者目录: 使用英文名或拼音，小写
- Skill 名称: 小写字母，连字符分隔

## 示例

```
skills/
├── skill-template/
├── zhangsan/
│   ├── weather-query/
│   └── data-analysis/
└── lisi/
    └── image-processing/
```
