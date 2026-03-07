#!/usr/bin/env python3
"""
HTML Dribbble Stylist Skill
创建具有 Dribbble 风格设计的精美 HTML 页面
"""

import json
import sys
from typing import Dict, Any, Optional


class DribbbleStylist:
    """Dribbble 风格 HTML 生成器"""
    
    def __init__(self):
        self.default_styles = {
            "background": "#f5f5f7",
            "card_bg": "#ffffff",
            "card_radius": "16px",
            "card_shadow": "0 2px 8px rgba(0,0,0,0.08)",
            "primary": "#667eea",
            "success": "#10b981",
            "warning": "#f59e0b",
            "danger": "#ef4444"
        }
    
    def create_page(self, title: str, content: Dict[str, Any], style: str = "card-layout") -> str:
        """
        创建 HTML 页面
        
        Args:
            title: 页面标题
            content: 内容数据
            style: 布局风格 (card-layout, dashboard, landing)
        
        Returns:
            完整的 HTML 字符串
        """
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: {self.default_styles['background']};
            min-height: 100vh;
            padding: 40px 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        h1 {{
            font-size: 32px;
            color: #1e293b;
            margin-bottom: 32px;
            text-align: center;
        }}
        
        .card {{
            background: {self.default_styles['card_bg']};
            border-radius: {self.default_styles['card_radius']};
            box-shadow: {self.default_styles['card_shadow']};
            padding: 24px;
            margin-bottom: 20px;
            opacity: 0;
            animation: fadeInUp 0.5s ease forwards;
        }}
        
        .card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        }}
        
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .status {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }}
        
        .status.success {{ background: #dcfce7; color: #166534; }}
        .status.active {{ background: #dbeafe; color: #1e40af; }}
        .status.warning {{ background: #fef3c7; color: #92400e; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <div class="card">
            <p>内容区域</p>
        </div>
    </div>
    <script>
        // 卡片依次动画
        document.querySelectorAll('.card').forEach((card, index) => {{
            card.style.animationDelay = `${{index * 0.1}}s`;
        }});
    </script>
</body>
</html>"""
        return html
    
    def save_page(self, html: str, filename: str) -> str:
        """保存 HTML 文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        return filename


def create_page(title: str, output: str = "output.html") -> str:
    """
    创建 Dribbble 风格 HTML 页面
    
    Args:
        title: 页面标题
        output: 输出文件名
    
    Returns:
        生成的文件路径
    """
    stylist = DribbbleStylist()
    html = stylist.create_page(title, {})
    stylist.save_page(html, output)
    return json.dumps({
        "status": "success",
        "file": output,
        "message": f"页面已生成: {output}"
    }, ensure_ascii=False, indent=2)


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("Usage: python skill.py create <title> [output.html]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "create":
        title = sys.argv[2] if len(sys.argv) > 2 else "My Page"
        output = sys.argv[3] if len(sys.argv) > 3 else "output.html"
        result = create_page(title, output)
        print(result)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
