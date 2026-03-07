#!/usr/bin/env python3
"""
云村 MCP Skill - 可运行版本
根据 README.md 文档实现
"""

import json
import ssl
import urllib.request
import urllib.error
from typing import Optional, Dict, Any

# ==================== 配置 ====================
# 替换为你的个人 token
TOKEN = "YOUR_TOKEN_HERE"
BASE_URL = f"https://opendata.igamegz.netease.com/mcp?token={TOKEN}"
PROTOCOL_VERSION = "2025-03-26"


class YuncunMCPClient:
    """云村 MCP 客户端"""
    
    def __init__(self, token: str = None):
        self.token = token or TOKEN
        if self.token == "YOUR_TOKEN_HERE":
            raise ValueError("请先设置 TOKEN 变量为你的个人 token")
        self.url = f"https://opendata.igamegz.netease.com/mcp?token={self.token}"
        self._request_id = 0
        self._ssl_context = ssl.create_default_context()
        self._ssl_context.check_hostname = False
        self._ssl_context.verify_mode = ssl.CERT_NONE
    
    def _call(self, method: str, params: Optional[Dict] = None) -> Any:
        """发送 MCP JSON-RPC 请求"""
        self._request_id += 1
        
        payload = {
            "jsonrpc": "2.0",
            "id": self._request_id,
            "method": method,
            "params": params or {}
        }
        
        data = json.dumps(payload).encode('utf-8')
        
        req = urllib.request.Request(
            self.url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=120, context=self._ssl_context) as response:
                result = json.loads(response.read().decode('utf-8'))
                if "error" in result:
                    raise Exception(f"MCP Error: {result['error']}")
                return result.get("result")
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            try:
                error_json = json.loads(error_body)
                raise Exception(f"HTTP {e.code}: {error_json.get('message', error_body)}")
            except json.JSONDecodeError:
                raise Exception(f"HTTP {e.code}: {error_body}")
    
    def _call_tool(self, tool_name: str, arguments: Dict) -> Any:
        """调用 MCP 工具"""
        result = self._call("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })
        
        if result and "content" in result:
            content = result["content"]
            if content and len(content) > 0:
                text = content[0].get("text", "")
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    return text
        return result
    
    def query_doris(self, sql: str, limit: int = 1000) -> Any:
        """使用 Doris 引擎执行 SQL 查询"""
        return self._call_tool("queryDataWithDoris", {
            "sql": sql,
            "type": "hive",
            "enableDialectConversion": True,
            "format": "json",
            "embedColumnNames": True,
            "limit": limit
        })
    
    def describe_table(self, table_name: str) -> Any:
        """获取表结构（使用 DESCRIBE）"""
        return self.query_doris(f"DESCRIBE {table_name}", limit=1000)


def main():
    """主函数 - 示例用法"""
    print("=" * 60)
    print("云村 MCP Skill")
    print("=" * 60)
    print()
    
    # 检查 token
    if TOKEN == "YOUR_TOKEN_HERE"::
        print("❌ 请先设置 TOKEN 变量为你的个人 token")
        print("编辑 skill.py 文件，将 TOKEN = \"YOUR_TOKEN_HERE\" 替换为你的实际 token")
        return
    
    try:
        client = YuncunMCPClient()
        
        # 示例1: 获取表结构
        print("示例1: 获取歌曲宽表结构")
        print("-" * 40)
        result = client.describe_table("music_new_dm.ads_itm_pgc_song_tag_dd")
        print(f"共 {len(result)} 个字段")
        print(f"前5个字段: {[f['Field'] for f in result[:5]]}")
        print()
        
        # 示例2: 查询歌曲总数
        print("示例2: 查询歌曲总数")
        print("-" * 40)
        result = client.query_doris("""
            SELECT 
                COUNT(*) as total_songs,
                COUNT(CASE WHEN is_ai_song = 1 THEN 1 END) as ai_songs
            FROM music_new_dm.ads_itm_pgc_song_tag_dd 
            WHERE dt = '2026-03-04'
        """)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print()
        
        # 示例3: 查询昨天播放最多的 AI 歌曲
        print("示例3: 昨天播放最多的 AI 歌曲 Top 5")
        print("-" * 40)
        result = client.query_doris("""
            SELECT 
                song_id,
                song_name,
                play_cnt_1d as yesterday_plays
            FROM music_new_dm.ads_itm_pgc_song_tag_dd 
            WHERE dt = '2026-03-04'
                AND is_ai_song = 1
            ORDER BY play_cnt_1d DESC
            LIMIT 5
        """)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ 错误: {e}")


if __name__ == "__main__":
    main()
