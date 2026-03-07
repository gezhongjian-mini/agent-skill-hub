# 贡献指南

感谢你对 Agent Skill Hub 的兴趣！以下是贡献指南。

## 🎯 贡献方式

### 1. 提交新 Skill

```bash
# 1. Fork 仓库并克隆
git clone https://github.com/your-org/agent-skill-hub.git
cd agent-skill-hub

# 2. 创建你的 skill 目录
mkdir -p skills/your-name/my-skill

# 3. 复制模板
cp -r skills/skill-template/* skills/your-name/my-skill/

# 4. 编辑文件
# - 修改 SKILL.md
# - 编写 src/main.py
# - 添加示例和测试

# 5. 验证
python scripts/validate-skill.py skills/your-name/my-skill

# 6. 更新注册表
python scripts/update-registry.py

# 7. 提交
git add .
git commit -m "Add: my-skill by your-name"
git push origin main
```

### 2. 更新现有 Skill

```bash
# 修改你的 skill
# 更新 metadata.json 中的版本号
# 更新 SKILL.md 的版本历史

python scripts/validate-skill.py skills/your-name/my-skill
python scripts/update-registry.py

git add .
git commit -m "Update: my-skill to v1.1.0"
git push
```

### 3. 报告问题

- 使用 GitHub Issues
- 描述问题
- 提供复现步骤

## 📝 Skill 规范

### 命名规范

- Skill 名称: 小写字母，连字符分隔 (`my-awesome-skill`)
- 目录结构: `skills/{author}/{skill-name}/`

### 代码规范

- 使用 Python 3.8+
- 遵循 PEP 8
- 添加类型注解
- 编写文档字符串

### 文档规范

SKILL.md 必须包含:
- 清晰的描述
- 完整的使用方法
- 参数说明表格
- 版本历史

## 🔍 代码审查

提交 PR 后，维护者会审查:
- 代码质量
- 文档完整性
- 测试覆盖率
- 命名规范

## 💡 建议

- 保持 Skill 单一职责
- 提供清晰的示例
- 编写测试用例
- 及时更新文档

## 📞 联系方式

有问题请联系项目维护者。
