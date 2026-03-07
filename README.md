# 🤖 Agent Skill Hub

一个用于团队成员共享、发现和更新 Agent Skill 的协作平台。

## 📋 项目简介

Agent Skill Hub 是一个中心化的 Skill 管理系统，帮助团队成员：
- 📤 **上传** 自己开发的 Agent Skill
- 🔍 **查询** 团队已有的 Skill
- 🔄 **更新** 现有 Skill 版本
- ⭐ **评价** Skill 质量

## 🗂️ 项目结构

```
agent-skill-hub/
├── README.md                 # 项目说明
├── skills/                   # Skill 存储目录
│   ├── README.md            # Skill 目录说明
│   ├── skill-template/      # Skill 模板
│   │   ├── SKILL.md         # Skill 文档模板
│   │   ├── src/             # 源代码
│   │   └── examples/        # 使用示例
│   └── [team-member]/       # 按成员分类
│       └── [skill-name]/
├── registry.json            # Skill 注册表
├── docs/                    # 文档
│   ├── contribution-guide.md # 贡献指南
│   ├── skill-spec.md        # Skill 规范
│   └── best-practices.md    # 最佳实践
└── scripts/                 # 工具脚本
    ├── validate-skill.py    # Skill 验证
    ├── search-skill.py      # Skill 搜索
    └── update-registry.py   # 更新注册表
```

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/your-org/agent-skill-hub.git
cd agent-skill-hub
```

### 2. 查看已有 Skill

```bash
# 查看所有 Skill
python scripts/search-skill.py --list

# 搜索特定 Skill
python scripts/search-skill.py --query "weather"
```

### 3. 上传新 Skill

```bash
# 1. 复制模板
cp -r skills/skill-template skills/[your-name]/my-skill

# 2. 编辑 SKILL.md 和代码
# ...

# 3. 验证 Skill
python scripts/validate-skill.py skills/[your-name]/my-skill

# 4. 更新注册表
python scripts/update-registry.py

# 5. 提交 PR
git add .
git commit -m "Add: my-skill by [your-name]"
git push origin main
```

## 📦 Skill 规范

每个 Skill 必须包含：

```
skill-name/
├── SKILL.md              # Skill 文档（必需）
├── src/                  # 源代码
│   └── main.py          # 主入口
├── examples/            # 使用示例
│   └── example.md
├── tests/               # 测试
│   └── test_skill.py
└── metadata.json        # 元数据
```

### SKILL.md 模板

```markdown
# Skill Name

## 描述
简要描述这个 Skill 的功能

## 作者
- 姓名: Your Name
- 邮箱: your.email@example.com
- 日期: 2024-01-01

## 功能
- 功能1: 描述
- 功能2: 描述

## 使用方法
\`\`\`bash
# 使用示例
\`\`\`

## 依赖
- dependency1
- dependency2

## 版本历史
- v1.0.0 (2024-01-01): 初始版本
```

## 🔍 查询 Skill

### 按名称搜索
```bash
python scripts/search-skill.py --name "weather"
```

### 按作者搜索
```bash
python scripts/search-skill.py --author "zhangsan"
```

### 按标签搜索
```bash
python scripts/search-skill.py --tag "api"
```

## 🔄 更新 Skill

1. 修改你的 Skill 文件
2. 更新 `SKILL.md` 中的版本历史
3. 运行验证脚本
4. 提交更新

```bash
git add skills/[your-name]/[skill-name]/
git commit -m "Update: [skill-name] to v1.1.0"
git push
```

## 🤝 贡献指南

1. **Fork** 这个仓库
2. 创建你的 Skill 分支 (`git checkout -b skill/my-skill`)
3. 添加你的 Skill
4. 确保通过验证 (`python scripts/validate-skill.py`)
5. 提交更改 (`git commit -am 'Add: my-skill'`)
6. 推送到分支 (`git push origin skill/my-skill`)
7. 创建 Pull Request

## 📊 Registry 格式

`registry.json` 包含所有注册的 Skill：

```json
{
  "version": "1.0.0",
  "lastUpdated": "2024-01-01T00:00:00Z",
  "skills": [
    {
      "id": "unique-skill-id",
      "name": "skill-name",
      "author": "author-name",
      "version": "1.0.0",
      "path": "skills/author-name/skill-name",
      "description": "Skill description",
      "tags": ["api", "weather"],
      "created": "2024-01-01T00:00:00Z",
      "updated": "2024-01-01T00:00:00Z"
    }
  ]
}
```

## 🛡️ 最佳实践

- ✅ 使用清晰的命名
- ✅ 编写完整的文档
- ✅ 提供使用示例
- ✅ 包含测试用例
- ✅ 定期更新版本
- ✅ 遵循代码规范

## 📞 联系方式

- 项目维护者: [Your Name]
- 邮箱: [your.email@example.com]
- 讨论区: [GitHub Discussions]

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件
