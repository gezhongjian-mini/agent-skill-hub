## 使用示例

### 示例 1: 获取表结构
```python
from src.skill import YuncunMCPClient

client = YuncunMCPClient(token="your-token")
result = client.describe_table("music_new_dm.ads_itm_pgc_song_tag_dd")
print(f"共 {len(result)} 个字段")
```

### 示例 2: 查询歌曲总数
```python
result = client.query_doris("""
    SELECT COUNT(*) as total_songs
    FROM music_new_dm.ads_itm_pgc_song_tag_dd 
    WHERE dt = '2026-03-04'
""")
```

### 示例 3: 查询 AI 歌曲 Top 5
```python
result = client.query_doris("""
    SELECT song_id, song_name, play_cnt_1d 
    FROM music_new_dm.ads_itm_pgc_song_tag_dd 
    WHERE dt = '2026-03-04' AND is_ai_song = 1
    ORDER BY play_cnt_1d DESC
    LIMIT 5
""")
```
