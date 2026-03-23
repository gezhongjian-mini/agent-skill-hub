#!/usr/bin/env python3
"""
OpenClaw Monitor Skill
生成自包含的 HTML 监控看板
"""

import json
import os
import subprocess
import argparse
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler


class OpenClawMonitor:
    """OpenClaw 监控看板"""
    
    def __init__(self):
        self.home_dir = os.path.expanduser("~/.openclaw")
        self.config_file = os.path.join(self.home_dir, "openclaw.json")
        self.sessions_file = os.path.join(self.home_dir, "agents/main/sessions/sessions.json")
        self.cron_file = os.path.join(self.home_dir, "cron/jobs.json")
        self.log_file = os.path.join(self.home_dir, "logs/gateway.log")
        self.skills_dir = "/opt/homebrew/lib/node_modules/openclaw/skills"
    
    def get_version(self):
        """获取 OpenClaw 版本"""
        try:
            result = subprocess.run(
                ['openclaw', '--version'],
                capture_output=True, text=True
            )
            return result.stdout.strip() or "Unknown"
        except:
            return "Unknown"
    
    def get_plugins(self):
        """获取插件信息"""
        try:
            result = subprocess.run(
                ['openclaw', 'config', 'get', 'plugins'],
                capture_output=True, text=True
            )
            plugins_data = json.loads(result.stdout)
            return [
                {
                    "name": name,
                    "version": info.get("resolvedVersion", "unknown"),
                    "enabled": info.get("enabled", False)
                }
                for name, info in plugins_data.get("entries", {}).items()
            ]
        except:
            return []
    
    def get_skills(self):
        """获取所有 Skills 及启用状态"""
        enabled_skills = set()
        
        # 读取启用的 skills
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                if 'agents' in config and 'list' in config['agents']:
                    for agent in config['agents']['list']:
                        if 'skills' in agent:
                            enabled_skills.update(agent['skills'])
        except:
            pass
        
        # 扫描所有 skills
        skills = []
        if os.path.isdir(self.skills_dir):
            for name in sorted(os.listdir(self.skills_dir)):
                path = os.path.join(self.skills_dir, name)
                if os.path.isdir(path):
                    skills.append({
                        "name": name,
                        "path": path,
                        "enabled": name in enabled_skills
                    })
        
        return skills
    
    def get_cron_tasks(self):
        """获取定时任务"""
        try:
            with open(self.cron_file, 'r') as f:
                cron_data = json.load(f)
            
            tasks = []
            for job in cron_data.get('jobs', []):
                job_id = job.get('id', 'unknown')
                last_run_ms = job.get('state', {}).get('lastRunAtMs')
                next_run_ms = job.get('state', {}).get('nextRunAtMs')
                
                last_run = '从未执行'
                if last_run_ms:
                    last_run = datetime.fromtimestamp(last_run_ms/1000).strftime('%Y-%m-%d %H:%M')
                
                next_run = '未知'
                if next_run_ms:
                    next_run = datetime.fromtimestamp(next_run_ms/1000).strftime('%m-%d %H:%M')
                
                tasks.append({
                    'id': job_id,
                    'name': job.get('name', '未命名'),
                    'schedule': job.get('schedule', {}).get('expr', '未知'),
                    'enabled': job.get('enabled', False),
                    'last_run': last_run,
                    'next_run': next_run,
                    'status': job.get('state', {}).get('lastRunStatus', 'unknown')
                })
            return tasks
        except:
            return []
    
    def get_session_info(self):
        """获取会话信息"""
        try:
            import time
            with open(self.sessions_file, 'r') as f:
                sessions = json.load(f)
            
            latest_session = None
            latest_time = 0
            
            for session_key, session_data in sessions.items():
                if isinstance(session_data, dict):
                    updated_at = session_data.get('updatedAt', 0)
                    if updated_at > latest_time:
                        latest_time = updated_at
                        latest_session = {
                            'id': session_key[:8] + '...',
                            'started': datetime.fromtimestamp(
                                session_data.get('startedAt', 0)/1000
                            ).strftime('%Y-%m-%d %H:%M') if session_data.get('startedAt') else 'N/A',
                            'updated': datetime.fromtimestamp(updated_at/1000).strftime('%H:%M:%S'),
                            'workspace': session_data.get('workspaceDir', 'unknown').split('/')[-1] if session_data.get('workspaceDir') else 'unknown',
                            'status': 'active' if (time.time() * 1000 - updated_at) < 300000 else 'inactive'
                        }
            
            return latest_session or {'status': 'no_session'}
        except:
            return {'status': 'error'}
    
    def get_heartbeat(self):
        """获取心跳信息"""
        try:
            with open(self.sessions_file, 'r') as f:
                sessions = json.load(f)
            
            update_times = []
            for session_data in sessions.values():
                if isinstance(session_data, dict):
                    updated_at = session_data.get('updatedAt', 0)
                    if updated_at:
                        update_times.append(updated_at)
            
            unique_times = sorted(set(update_times), reverse=True)
            recent = [
                datetime.fromtimestamp(ts/1000).strftime('%H:%M:%S')
                for ts in unique_times[:3]
            ]
            
            return {
                'recent': recent,
                'count': len(unique_times),
                'last': recent[0] if recent else 'N/A'
            }
        except:
            return {'recent': [], 'count': 0, 'last': 'N/A'}
    
    def get_logs(self, lines=100):
        """获取日志"""
        try:
            if not os.path.exists(self.log_file):
                return []
            
            with open(self.log_file, 'r') as f:
                all_lines = f.readlines()
            
            return [line.strip() for line in all_lines[-lines:] if line.strip()]
        except:
            return []
    
    def collect_data(self):
        """收集所有监控数据"""
        return {
            'version': self.get_version(),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'plugins': self.get_plugins(),
            'skills': self.get_skills(),
            'cron_tasks': self.get_cron_tasks(),
            'session': self.get_session_info(),
            'heartbeat': self.get_heartbeat(),
            'logs': self.get_logs(50)
        }
    
    def generate_html(self, data):
        """生成 HTML 监控面板"""
        # 统计信息
        enabled_plugins = sum(1 for p in data['plugins'] if p['enabled'])
        enabled_skills = sum(1 for s in data['skills'] if s['enabled'])
        enabled_cron = sum(1 for c in data['cron_tasks'] if c['enabled'])
        
        # 插件列表 HTML
        plugins_html = ""
        for p in data['plugins']:
            status_class = "success" if p['enabled'] else "muted"
            status_icon = "●" if p['enabled'] else "○"
            plugins_html += f"""
                <div class="item">
                    <span class="item-status {status_class}">{status_icon}</span>
                    <span class="item-name">{p['name']}</span>
                    <span class="item-meta">{p['version']}</span>
                </div>
            """
        
        # Skills 列表 HTML
        skills_html = ""
        for s in data['skills']:
            status_class = "success" if s['enabled'] else "muted"
            status_text = "已启用" if s['enabled'] else "未启用"
            skills_html += f"""
                <div class="item">
                    <span class="item-status {status_class}">{'●' if s['enabled'] else '○'}</span>
                    <span class="item-name">{s['name']}</span>
                    <span class="badge {status_class}">{status_text}</span>
                </div>
            """
        
        # 定时任务 HTML
        cron_html = ""
        for c in data['cron_tasks']:
            status_class = "success" if c['enabled'] else "warning"
            cron_html += f"""
                <div class="item">
                    <span class="item-status {status_class}">{'●' if c['enabled'] else '○'}</span>
                    <span class="item-name">{c['name']}</span>
                    <span class="item-meta">{c['schedule']}</span>
                </div>
            """
        
        # 日志 HTML
        logs_html = ""
        for log in data['logs']:
            logs_html += f"<div class=\"log-line\">{self._escape_html(log)}</div>\n"
        
        # 心跳 HTML
        heartbeat_html = ""
        for hb in data['heartbeat']['recent']:
            heartbeat_html += f"<div class=\"heartbeat-item\">{hb}</div>"
        
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenClaw Monitor</title>
    <style>
        :root {{
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-card: rgba(26, 26, 37, 0.8);
            --border: rgba(255, 255, 255, 0.08);
            --text: #f0f0f5;
            --text-secondary: #a0a0b0;
            --text-muted: #6a6a80;
            --accent: #6366f1;
            --success: #10b981;
            --warning: #f59e0b;
            --error: #ef4444;
        }}
        
        [data-theme="light"] {{
            --bg-primary: #f8f9fa;
            --bg-secondary: #ffffff;
            --bg-card: rgba(255, 255, 255, 0.9);
            --border: rgba(0, 0, 0, 0.08);
            --text: #212529;
            --text-secondary: #495057;
            --text-muted: #868e96;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg-primary);
            color: var(--text);
            min-height: 100vh;
            padding: 20px;
            line-height: 1.6;
        }}
        
        .container {{ max-width: 1400px; margin: 0 auto; }}
        
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border);
        }}
        
        h1 {{
            font-size: 24px;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .timestamp {{
            font-size: 12px;
            color: var(--text-muted);
            font-family: monospace;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }}
        
        .panel {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
        }}
        
        .panel-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }}
        
        .panel-title {{
            font-size: 14px;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .panel-badge {{
            font-size: 11px;
            padding: 4px 8px;
            background: var(--bg-secondary);
            border-radius: 20px;
            color: var(--text-muted);
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }}
        
        .stat {{
            background: var(--bg-secondary);
            border-radius: 8px;
            padding: 16px;
        }}
        
        .stat-value {{
            font-size: 24px;
            font-weight: 700;
            font-family: monospace;
        }}
        
        .stat-label {{
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 4px;
        }}
        
        .item {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 0;
            border-bottom: 1px solid var(--border);
        }}
        
        .item:last-child {{ border-bottom: none; }}
        
        .item-status {{ font-size: 10px; }}
        
        .item-name {{ flex: 1; font-size: 14px; }}
        
        .item-meta {{
            font-size: 12px;
            color: var(--text-muted);
            font-family: monospace;
        }}
        
        .badge {{
            font-size: 11px;
            padding: 2px 8px;
            border-radius: 4px;
            background: var(--bg-secondary);
        }}
        
        .success {{ color: var(--success); }}
        .warning {{ color: var(--warning); }}
        .error {{ color: var(--error); }}
        .muted {{ color: var(--text-muted); }}
        
        .logs {{
            background: var(--bg-secondary);
            border-radius: 8px;
            padding: 12px;
            max-height: 300px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 12px;
        }}
        
        .log-line {{
            padding: 4px 0;
            border-bottom: 1px solid var(--border);
            color: var(--text-secondary);
        }}
        
        .session-info {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        
        .session-row {{
            display: flex;
            justify-content: space-between;
            font-size: 13px;
        }}
        
        .session-label {{ color: var(--text-muted); }}
        
        .session-value {{
            font-family: monospace;
            color: var(--text-secondary);
        }}
        
        .heartbeat-list {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        
        .heartbeat-item {{
            font-family: monospace;
            font-size: 13px;
            color: var(--text-secondary);
            padding: 6px 10px;
            background: var(--bg-secondary);
            border-radius: 6px;
        }}
        
        .theme-toggle {{
            display: flex;
            gap: 8px;
        }}
        
        .theme-btn {{
            padding: 6px 12px;
            border: 1px solid var(--border);
            background: var(--bg-secondary);
            color: var(--text-secondary);
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
        }}
        
        .theme-btn:hover {{
            border-color: var(--accent);
            color: var(--text);
        }}
        
        .full-width {{ grid-column: 1 / -1; }}
    </style>
</head>
<body data-theme="dark">
    <div class="container">
        <header>
            <div>
                <h1>🎯 OpenClaw Monitor</h1>
                <div class="timestamp">生成时间: {data['timestamp']} | 版本: {data['version']}</div>
            </div>
            <div class="theme-toggle">
                <button class="theme-btn" onclick="setTheme('dark')">🌙</button>
                <button class="theme-btn" onclick="setTheme('light')">☀️</button>
                <button class="theme-btn" onclick="setTheme('auto')">Auto</button>
            </div>
        </header>
        
        <div class="grid">
            <!-- 系统概览 -->
            <div class="panel">
                <div class="panel-header">
                    <span class="panel-title">📊 系统概览</span>
                </div>
                <div class="stats">
                    <div class="stat">
                        <div class="stat-value success">{enabled_plugins}</div>
                        <div class="stat-label">已启用插件</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value success">{enabled_skills}</div>
                        <div class="stat-label">已启用 Skills</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">{len(data['skills'])}</div>
                        <div class="stat-label">总 Skills</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value warning">{enabled_cron}</div>
                        <div class="stat-label">定时任务</div>
                    </div>
                </div>
            </div>
            
            <!-- 会话信息 -->
            <div class="panel">
                <div class="panel-header">
                    <span class="panel-title">💬 会话信息</span>
                    <span class="panel-badge">{data['session'].get('status', 'unknown')}</span>
                </div>
                <div class="session-info">
                    <div class="session-row">
                        <span class="session-label">ID</span>
                        <span class="session-value">{data['session'].get('id', 'N/A')}</span>
                    </div>
                    <div class="session-row">
                        <span class="session-label">启动时间</span>
                        <span class="session-value">{data['session'].get('started', 'N/A')}</span>
                    </div>
                    <div class="session-row">
                        <span class="session-label">最后更新</span>
                        <span class="session-value">{data['session'].get('updated', 'N/A')}</span>
                    </div>
                    <div class="session-row">
                        <span class="session-label">工作区</span>
                        <span class="session-value">{data['session'].get('workspace', 'unknown')}</span>
                    </div>
                </div>
            </div>
            
            <!-- 心跳监控 -->
            <div class="panel">
                <div class="panel-header">
                    <span class="panel-title">💓 心跳监控</span>
                    <span class="panel-badge">{data['heartbeat']['count']} sessions</span>
                </div>
                <div class="heartbeat-list">
                    {heartbeat_html if heartbeat_html else '<div class="heartbeat-item">暂无数据</div>'}
                </div>
            </div>
            
            <!-- 插件列表 -->
            <div class="panel">
                <div class="panel-header">
                    <span class="panel-title">🔌 插件</span>
                    <span class="panel-badge">{len(data['plugins'])}</span>
                </div>
                {plugins_html if plugins_html else '<div class="item"><span class="item-name muted">暂无插件</span></div>'}
            </div>
            
            <!-- Skills 列表 -->
            <div class="panel">
                <div class="panel-header">
                    <span class="panel-title">🛠️ Skills</span>
                    <span class="panel-badge">{len(data['skills'])}</span>
                </div>
                {skills_html if skills_html else '<div class="item"><span class="item-name muted">暂无 Skills</span></div>'}
            </div>
            
            <!-- 定时任务 -->
            <div class="panel">
                <div class="panel-header">
                    <span class="panel-title">⏰ 定时任务</span>
                    <span class="panel-badge">{len(data['cron_tasks'])}</span>
                </div>
                {cron_html if cron_html else '<div class="item"><span class="item-name muted">暂无定时任务</span></div>'}
            </div>
            
            <!-- 系统日志 -->
            <div class="panel full-width">
                <div class="panel-header">
                    <span class="panel-title">📝 系统日志 (最近 50 条)</span>
                </div>
                <div class="logs">
                    {logs_html if logs_html else '<div class="log-line muted">暂无日志</div>'}
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function setTheme(theme) {{
            if (theme === 'auto') {{
                const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                document.body.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
            }} else {{
                document.body.setAttribute('data-theme', theme);
            }}
        }}
    </script>
</body>
</html>'''
        return html
    
    def _escape_html(self, text):
        """转义 HTML 特殊字符"""
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    def save_html(self, html, output_path):
        """保存 HTML 文件"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ Dashboard saved to: {output_path}")
    
    def serve(self, port=8891):
        """启动 HTTP 服务"""
        class Handler(SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    data = self.server.monitor.collect_data()
                    html = self.server.monitor.generate_html(data)
                    self.wfile.write(html.encode())
                elif self.path == '/api/data':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    data = self.server.monitor.collect_data()
                    self.wfile.write(json.dumps(data).encode())
                else:
                    self.send_error(404)
            
            def log_message(self, format, *args):
                pass
        
        server = HTTPServer(('', port), Handler)
        server.monitor = self
        print(f"🚀 Server running at http://localhost:{port}")
        print("Press Ctrl+C to stop")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped")


def main():
    parser = argparse.ArgumentParser(description='OpenClaw Monitor')
    parser.add_argument('--output', '-o', default='openclaw-monitor.html', help='输出文件路径')
    parser.add_argument('--serve', '-s', action='store_true', help='启动 HTTP 服务')
    parser.add_argument('--port', '-p', type=int, default=8891, help='服务端口')
    args = parser.parse_args()
    
    monitor = OpenClawMonitor()
    
    if args.serve:
        monitor.serve(args.port)
    else:
        data = monitor.collect_data()
        html = monitor.generate_html(data)
        monitor.save_html(html, args.output)


if __name__ == '__main__':
    main()
