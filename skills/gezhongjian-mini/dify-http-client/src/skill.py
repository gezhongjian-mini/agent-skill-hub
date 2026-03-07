#!/usr/bin/env python3
"""
Dify Assistant Skill
综合 Workflow 和 Chat 两种调用方式
"""

import json
import sys
import time
import requests
from typing import Optional, Dict, Any


class DifyAssistant:
    """Dify 助手 - 支持 Workflow 和 Chat 两种模式"""
    
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key
        self.base_url = base_url or "http://dify-beta.panshi-gy.netease.com/v1"
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            })
    
    # ========== Workflow API ==========
    
    def workflow_run(self, run_type: str = "实时", user: str = "openclaw-test") -> Dict[str, Any]:
        """
        执行 Workflow
        
        Args:
            run_type: "实时" 或 "异步"
            user: 用户标识
        
        Returns:
            执行结果（实时模式）或任务信息（异步模式）
        """
        url = f"{self.base_url}/workflows/run"
        
        data = {
            "inputs": {"type": run_type},
            "response_mode": "blocking",
            "user": user
        }
        
        response = self.session.post(url, json=data, timeout=300)
        response.raise_for_status()
        return response.json()
    
    def workflow_query(self, workflow_run_id: str) -> Dict[str, Any]:
        """
        查询 Workflow 执行结果
        
        Args:
            workflow_run_id: Workflow 执行 ID
        
        Returns:
            执行状态和结果
        """
        url = f"{self.base_url}/workflows/run/{workflow_run_id}"
        
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    
    def workflow_run_and_wait(
        self,
        run_type: str = "实时",
        user: str = "openclaw-test",
        poll_interval: int = 60,
        max_wait: int = 600
    ) -> Dict[str, Any]:
        """
        执行 Workflow 并等待完成（支持异步模式轮询）
        
        Args:
            run_type: "实时" 或 "异步"
            user: 用户标识
            poll_interval: 轮询间隔（秒）
            max_wait: 最大等待时间（秒）
        
        Returns:
            最终执行结果
        """
        # 提交任务
        result = self.workflow_run(run_type, user)
        
        # 实时模式直接返回
        if run_type == "实时":
            return result
        
        # 异步模式需要轮询
        workflow_run_id = result.get("workflow_run_id")
        print(f"异步任务已提交: {workflow_run_id}")
        print(f"开始轮询，间隔 {poll_interval} 秒...")
        
        start_time = time.time()
        while time.time() - start_time < max_wait:
            status_result = self.workflow_query(workflow_run_id)
            status = status_result.get("status")
            elapsed = status_result.get("elapsed_time", 0)
            steps = status_result.get("total_steps", 0)
            
            print(f"[{time.strftime('%H:%M:%S')}] Status: {status}, Steps: {steps}, Elapsed: {elapsed:.2f}s")
            
            if status == "succeeded":
                print(f"✅ 任务完成！")
                return status_result
            elif status in ("failed", "stopped"):
                print(f"❌ 任务失败: {status_result.get('error')}")
                return status_result
            
            time.sleep(poll_interval)
        
        print(f"⏰ 等待超时")
        return status_result
    
    # ========== Chat API ==========
    
    def chat(self, query: str, user: str = "openclaw-test", timeout: int = 120) -> Dict[str, Any]:
        """
        Chat 对话
        
        Args:
            query: 对话内容
            user: 用户标识
            timeout: 超时时间（秒）
        
        Returns:
            包含 answer 和 metadata 的完整响应
        """
        url = f"{self.base_url}/chat-messages"
        
        data = {
            "inputs": {},
            "query": query,
            "response_mode": "blocking",
            "conversation_id": "",
            "user": user
        }
        
        response = self.session.post(url, json=data, timeout=timeout)
        response.raise_for_status()
        return response.json()
    
    def chat_sql(self, sql: str, user: str = "openclaw-test", timeout: int = 120) -> Dict[str, Any]:
        """
        使用 Chat 模式执行 SQL 查询
        
        Args:
            sql: SQL 查询语句
            user: 用户标识
            timeout: 超时时间（秒）
        
        Returns:
            包含格式化结果的响应
        """
        return self.chat(sql, user, timeout)


# ========== Skill Tool Functions ==========

def dify_workflow_realtime(
    api_key: str = "app-1QqjBYvVZrvEqRREoN8vL64n",
    base_url: str = "http://dify-beta.panshi-gy.netease.com/v1",
    type: str = "实时",
    user: str = "openclaw-test"
) -> str:
    """
    执行 Dify Workflow（实时模式）
    
    Args:
        api_key: Dify Workflow API Key
        base_url: Dify API 基础地址
        type: 执行类型（实时/异步）
        user: 用户标识
    
    Returns:
        JSON 格式的执行结果
    """
    assistant = DifyAssistant(api_key, base_url)
    result = assistant.workflow_run(type, user)
    return json.dumps(result, ensure_ascii=False, indent=2)


def dify_workflow_async(
    api_key: str = "app-1QqjBYvVZrvEqRREoN8vL64n",
    base_url: str = "http://dify-beta.panshi-gy.netease.com/v1",
    user: str = "openclaw-test"
) -> str:
    """
    执行 Dify Workflow（异步模式），返回任务ID
    
    Args:
        api_key: Dify Workflow API Key
        base_url: Dify API 基础地址
        user: 用户标识
    
    Returns:
        JSON 格式的任务信息（包含 workflow_run_id）
    """
    assistant = DifyAssistant(api_key, base_url)
    result = assistant.workflow_run("异步", user)
    return json.dumps(result, ensure_ascii=False, indent=2)


def dify_workflow_query(
    workflow_run_id: str,
    api_key: str = "app-1QqjBYvVZrvEqRREoN8vL64n",
    base_url: str = "http://dify-beta.panshi-gy.netease.com/v1"
) -> str:
    """
    查询异步 Workflow 执行结果
    
    Args:
        workflow_run_id: Workflow 执行 ID（由异步模式返回）
        api_key: Dify Workflow API Key
        base_url: Dify API 基础地址
    
    Returns:
        JSON 格式的执行状态和结果
    """
    assistant = DifyAssistant(api_key, base_url)
    result = assistant.workflow_query(workflow_run_id)
    return json.dumps(result, ensure_ascii=False, indent=2)


def dify_chat_sql(
    sql: str,
    api_key: str = "app-OuRmNS25dU8wUN0t0TFpTRq9",
    base_url: str = "http://dify-beta.panshi-gy.netease.com/v1",
    user: str = "openclaw-test"
) -> str:
    """
    使用 Dify Chat（SQL助手）执行 SQL 查询
    
    Args:
        sql: SQL 查询语句
        api_key: Dify Chat API Key
        base_url: Dify API 基础地址
        user: 用户标识
    
    Returns:
        JSON 格式的查询结果（包含格式化的 answer）
    """
    assistant = DifyAssistant(api_key, base_url)
    result = assistant.chat_sql(sql, user)
    return json.dumps(result, ensure_ascii=False, indent=2)


def dify_chat(
    query: str,
    api_key: str = "app-OuRmNS25dU8wUN0t0TFpTRq9",
    base_url: str = "http://dify-beta.panshi-gy.netease.com/v1",
    user: str = "openclaw-test"
) -> str:
    """
    使用 Dify Chat 进行对话
    
    Args:
        query: 对话内容/问题
        api_key: Dify Chat API Key
        base_url: Dify API 基础地址
        user: 用户标识
    
    Returns:
        JSON 格式的对话结果
    """
    assistant = DifyAssistant(api_key, base_url)
    result = assistant.chat(query, user)
    return json.dumps(result, ensure_ascii=False, indent=2)


# ========== Command Line Interface ==========

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("Usage: python3 skill.py <function> [args...]")
        print("\nAvailable functions:")
        print("  dify_workflow_realtime [type] [user]")
        print("  dify_workflow_async [user]")
        print("  dify_workflow_query <workflow_run_id>")
        print("  dify_chat_sql <sql>")
        print("  dify_chat <query>")
        sys.exit(1)
    
    func_name = sys.argv[1]
    args = sys.argv[2:]
    
    try:
        if func_name == "dify_workflow_realtime":
            result = dify_workflow_realtime(
                type=args[0] if len(args) > 0 else "实时",
                user=args[1] if len(args) > 1 else "openclaw-test"
            )
            print(result)
        
        elif func_name == "dify_workflow_async":
            result = dify_workflow_async(
                user=args[0] if len(args) > 0 else "openclaw-test"
            )
            print(result)
        
        elif func_name == "dify_workflow_query":
            if len(args) < 1:
                print("Error: workflow_run_id required")
                sys.exit(1)
            result = dify_workflow_query(args[0])
            print(result)
        
        elif func_name == "dify_chat_sql":
            if len(args) < 1:
                print("Error: sql required")
                sys.exit(1)
            result = dify_chat_sql(args[0])
            print(result)
        
        elif func_name == "dify_chat":
            if len(args) < 1:
                print("Error: query required")
                sys.exit(1)
            result = dify_chat(args[0])
            print(result)
        
        else:
            print(f"Unknown function: {func_name}")
            sys.exit(1)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
