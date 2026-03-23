---
name: openclaw-monitor
description: OpenClaw 监控看板。当用户需要查看 OpenClaw 运行状态、插件列表、启用 Skills、定时任务、会话信息或系统日志时触发。生成自包含的 HTML 监控面板。
---

# OpenClaw Monitor Skill

## 描述
OpenClaw 监控看板 Skill，用于实时展示 OpenClaw 系统运行状态。生成一个自包含的 HTML 监控面板，支持暗黑/亮色主题切换。

## 作者
- 姓名: gezhongjian-mini
- 日期: 2026-03-23

## 功能
- **系统概览**: OpenClaw 版本、运行时间、系统状态
- **插件监控**: 显示所有已安装插件及其启用状态
- **Skills 管理**: 列出所有可用 Skills，标记已启用项
- **定时任务**: 展示 cron 任务配置及最近执行历史
- **会话信息**: 当前活跃会话详情
- **心跳监控**: 最近活跃时间追踪
- **日志查看器**: 实时查看系统日志（支持过滤和搜索）
- **主题切换**: 支持 Dark/Light/Auto 三种主题

## 使用方法

### 命令行
```bash
# 生成监控看板
python src/main.py

# 指定输出文件
python src/main.py --output /path/to/dashboard.html

# 启动 HTTP 服务（带实时 API）
python src/main.py --serve --port 8891
```

### Python API
```python
from src.main import OpenClawMonitor

monitor = OpenClawMonitor()

# 获取系统数据
data = monitor.collect_data()

# 生成 HTML 看板
html = monitor.generate_html(data)
monitor.save_html(html, "dashboard.html")

# 或启动服务
monitor.serve(port=8891)
```

## 监控面板布局

```
┌─────────────────────────────────────────────────────────────┐
│  OpenClaw Monitor v1.0                    [Dark/Light/Auto] │
├───────────────┬───────────────┬─────────────────────────────┤
│  系统概览      │  插件状态      │  心跳监控                   │
│  - 版本       │  - moltbot-popo│  - 最近活跃时间              │
│  - 运行时间    │  - minimax-auth│  - 活跃会话数                │
│  - 状态       │                │                             │
├───────────────┼───────────────┼─────────────────────────────┤
│  Skills 列表  │  定时任务      │  会话信息                   │
│  - skill-creator        │  - workspace-inspector        │
│  - n8n-workflows        │  - daily-memory               │
│  - ...                  │  - 下次执行时间               │
│                         │  - 最近执行历史               │
├─────────────────────────┴─────────────────────────────────┤
│  系统日志查看器 (支持搜索/过滤/实时刷新)                    │
└─────────────────────────────────────────────────────────────┘
```

## 数据源

| 数据类型 | 来源路径 |
|---------|---------|
| 插件信息 | `~/.openclaw/config/plugins` |
| Skills | `/opt/homebrew/lib/node_modules/openclaw/skills/` |
| 启用 Skills | `~/.openclaw/openclaw.json` (agents.list[].skills) |
| 定时任务 | `~/.openclaw/cron/jobs.json` |
| 会话信息 | `~/.openclaw/agents/main/sessions/sessions.json` |
| 日志 | `~/.openclaw/logs/gateway.log` |

## 依赖
- Python >= 3.8
- 无第三方依赖（纯标准库）

## 文件结构
```
openclaw-monitor/
├── SKILL.md              # Skill 文档
├── metadata.json         # 元数据
└── src/
    └── main.py          # 主程序
```

## 版本历史
- v1.0.0 (2026-03-23): 初始版本，支持完整的监控面板功能
