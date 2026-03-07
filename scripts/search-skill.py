#!/usr/bin/env python3
"""
Skill 搜索工具
用于查询 registry 中的 skill
"""

import json
import argparse
import os
from pathlib import Path

REGISTRY_FILE = Path(__file__).parent.parent / "registry.json"
SKILLS_DIR = Path(__file__).parent.parent / "skills"


def load_registry():
    """加载注册表"""
    if not REGISTRY_FILE.exists():
        return {"skills": []}
    with open(REGISTRY_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def list_all_skills():
    """列出所有 skill"""
    registry = load_registry()
    skills = registry.get("skills", [])
    
    if not skills:
        print("暂无注册的 Skill")
        return
    
    print(f"\n共有 {len(skills)} 个 Skill:\n")
    print(f"{'名称':<20} {'作者':<15} {'版本':<10} {'描述'}")
    print("-" * 80)
    
    for skill in skills:
        print(f"{skill['name']:<20} {skill['author']:<15} {skill['version']:<10} {skill['description'][:30]}...")


def search_by_name(query):
    """按名称搜索"""
    registry = load_registry()
    skills = [s for s in registry.get("skills", []) if query.lower() in s['name'].lower()]
    
    if not skills:
        print(f"未找到包含 '{query}' 的 Skill")
        return
    
    print(f"\n找到 {len(skills)} 个匹配的 Skill:\n")
    for skill in skills:
        print_skill_detail(skill)


def search_by_author(author):
    """按作者搜索"""
    registry = load_registry()
    skills = [s for s in registry.get("skills", []) if author.lower() in s['author'].lower()]
    
    if not skills:
        print(f"未找到作者 '{author}' 的 Skill")
        return
    
    print(f"\n作者 '{author}' 的 Skill ({len(skills)} 个):\n")
    for skill in skills:
        print_skill_detail(skill)


def search_by_tag(tag):
    """按标签搜索"""
    registry = load_registry()
    skills = [s for s in registry.get("skills", []) if tag.lower() in [t.lower() for t in s.get('tags', [])]]
    
    if not skills:
        print(f"未找到标签 '{tag}' 的 Skill")
        return
    
    print(f"\n标签 '{tag}' 的 Skill ({len(skills)} 个):\n")
    for skill in skills:
        print_skill_detail(skill)


def print_skill_detail(skill):
    """打印 Skill 详情"""
    print(f"\n📦 {skill['name']} v{skill['version']}")
    print(f"   作者: {skill['author']}")
    print(f"   描述: {skill['description']}")
    print(f"   标签: {', '.join(skill.get('tags', []))}")
    print(f"   路径: {skill['path']}")
    print(f"   更新: {skill['updated']}")
    print()


def main():
    parser = argparse.ArgumentParser(description='Agent Skill Hub 搜索工具')
    parser.add_argument('--list', '-l', action='store_true', help='列出所有 Skill')
    parser.add_argument('--name', '-n', type=str, help='按名称搜索')
    parser.add_argument('--author', '-a', type=str, help='按作者搜索')
    parser.add_argument('--tag', '-t', type=str, help='按标签搜索')
    
    args = parser.parse_args()
    
    if args.list:
        list_all_skills()
    elif args.name:
        search_by_name(args.name)
    elif args.author:
        search_by_author(args.author)
    elif args.tag:
        search_by_tag(args.tag)
    else:
        list_all_skills()


if __name__ == '__main__':
    main()
