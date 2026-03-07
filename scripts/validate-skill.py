#!/usr/bin/env python3
"""
Skill 验证工具
验证 skill 是否符合规范
"""

import json
import sys
from pathlib import Path


def validate_skill(skill_path):
    """验证 skill 目录结构"""
    skill_path = Path(skill_path)
    
    if not skill_path.exists():
        print(f"❌ 路径不存在: {skill_path}")
        return False
    
    errors = []
    
    # 检查必需文件
    required_files = [
        "SKILL.md",
        "metadata.json"
    ]
    
    for file in required_files:
        if not (skill_path / file).exists():
            errors.append(f"缺少必需文件: {file}")
    
    # 检查 src 目录
    if not (skill_path / "src").exists():
        errors.append("缺少 src 目录")
    
    # 验证 metadata.json
    metadata_path = skill_path / "metadata.json"
    if metadata_path.exists():
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            required_fields = ['name', 'version', 'author', 'description']
            for field in required_fields:
                if field not in metadata:
                    errors.append(f"metadata.json 缺少字段: {field}")
        except json.JSONDecodeError:
            errors.append("metadata.json 格式错误")
    
    # 验证 SKILL.md
    skill_md_path = skill_path / "SKILL.md"
    if skill_md_path.exists():
        content = skill_md_path.read_text(encoding='utf-8')
        required_sections = ['描述', '作者', '功能', '使用方法']
        for section in required_sections:
            if section not in content:
                errors.append(f"SKILL.md 缺少章节: {section}")
    
    # 输出结果
    if errors:
        print(f"\n❌ {skill_path.name} 验证失败:")
        for error in errors:
            print(f"   - {error}")
        return False
    else:
        print(f"\n✅ {skill_path.name} 验证通过!")
        return True


def main():
    if len(sys.argv) < 2:
        print("用法: python validate-skill.py <skill-path>")
        print("示例: python validate-skill.py skills/zhangsan/my-skill")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    success = validate_skill(skill_path)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
