# 云村 MCP Skill

## 描述
云村 MCP (Model Context Protocol) 客户端 Skill，用于连接网易云音乐内部数据平台，执行 Doris SQL 查询。

## 作者
- 姓名: gezhongjian-mini
- 日期: 2026-03-07

## 功能
- **Doris SQL 查询**: 执行 SQL 并返回 JSON 结果
- **表结构获取**: 使用 DESCRIBE 获取表字段信息
- **AI 歌曲分析**: 查询 AI 歌曲播放数据

## 使用方法

### 配置
编辑 `src/skill.py`，设置你的 token：
```python
TOKEN = "your-token-here"
```

### 命令行
```bash
python src/skill.py
```

### Python API
```python
from src.skill import YuncunMCPClient

client = YuncunMCPClient(token="your-token")

# 查询表结构
result = client.describe_table("music_new_dm.ads_itm_pgc_song_tag_dd")

# 执行 SQL
result = client.query_doris("SELECT COUNT(*) FROM table")
```

## 常用表
- `music_new_dm.ads_itm_pgc_song_tag_dd` - 歌曲宽表
- `music_new_dm.ads_itm_pgc_singer_tag_dd` - 艺人宽表

## 依赖
- Python >= 3.8
- 无第三方依赖（使用标准库）

## 版本历史
- v1.0.0 (2026-03-07): 初始版本，支持 Doris 查询
