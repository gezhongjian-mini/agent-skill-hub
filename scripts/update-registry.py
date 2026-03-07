#!/usr/bin/env python3
"""
更新注册表工具
扫描 skills 目录并更新 registry.json
"""

import json
from pathlib import Path
from datetime import datetime

REGISTRY_FILE = Path(__file__).parent.parent / "registry.json"
SKILLS_DIR = Path(__file__).parent.parent / "skills"


def scan_skills():
    """扫描 skills 目录"""
    skills = []
    
    # 遍历所有成员目录
    for author_dir in SKILLS_DIR.iterdir():
        if not author_dir.is_dir() or author_dir.name == 'skill-template':
            continue
        
        # 遍历该成员的所有 skill
        for skill_dir in author_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            
            metadata_path = skill_dir / "metadata.json"
            if not metadata_path.exists():
                continue
            
            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                skill_info = {
                    "id": f"{author_dir.name}-{metadata['name']}",
                    "name": metadata['name'],
                    "author": metadata['author'],
                    "version": metadata['version'],
                    "path": f"skills/{author_dir.name}/{skill_dir.name}",
                    "description": metadata.get('description', ''),
                    "tags": metadata.get('tags', []),
                    "language": metadata.get('language', 'python'),
                    "created": metadata.get('created', datetime.now().isoformat()),
                    "updated": metadata.get('updated', datetime.now().isoformat())
                }
                skills.append(skill_info)
                
            except Exception as e:
                print(f"⚠️  读取 {skill_dir} 失败: {e}")
    
    return skills


def update_registry():
    """更新注册表"""
    # 加载现有注册表
    if REGISTRY_FILE.exists():
        with open(REGISTRY_FILE, 'r', encoding='utf-8') as f:
            registry = json.load(f)
    else:
        registry = {"version": "1.0.0", "skills": []}
    
    # 扫描 skills
    skills = scan_skills()
    
    # 更新注册表
    registry['skills'] = skills
    registry['lastUpdated'] = datetime.now().isoformat()
    registry['metadata'] = {
        "totalSkills": len(skills),
        "totalAuthors": len(set(s['author'] for s in skills)),
        "categories": list(set(tag for s in skills for tag in s.get('tags', [])))
    }
    
    # 保存
    with open(REGISTRY_FILE, 'w', encoding='utf-8') as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 注册表更新成功!")
    print(f"   总 Skill 数: {len(skills)}")
    print(f"   作者数: {registry['metadata']['totalAuthors']}")
    print(f"   标签: {', '.join(registry['metadata']['categories'])}")


if __name__ == '__main__':
    update_registry()
