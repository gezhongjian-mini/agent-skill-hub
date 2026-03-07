#!/usr/bin/env python3
"""
Skill 测试
"""

import unittest
import sys
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import MySkill


class TestMySkill(unittest.TestCase):
    """测试 MySkill"""
    
    def setUp(self):
        """测试前准备"""
        self.skill = MySkill()
    
    def test_run_success(self):
        """测试正常执行"""
        result = self.skill.run("test input")
        
        self.assertEqual(result['status'], 'success')
        self.assertIn('Processed', result['data'])
    
    def test_run_with_config(self):
        """测试带配置执行"""
        skill = MySkill(config={'timeout': 60})
        self.assertEqual(skill.timeout, 60)
    
    def test_run_empty_input(self):
        """测试空输入"""
        result = self.skill.run("")
        self.assertEqual(result['status'], 'success')


if __name__ == '__main__':
    unittest.main()
