#!/usr/bin/env python3
"""
GitHub Token Test Script
测试 GitHub Personal Access Token 的有效性和权限
"""

import os
import requests
import json
import sys

def test_token():
    # 从环境变量获取 token
    token = os.environ.get('PRIVATE_REPO_TOKEN', '')
    
    if not token:
        print("❌ PRIVATE_REPO_TOKEN 环境变量未设置")
        return False
    
    print(f"🔍 检测到 Token: {token[:8]}...{token[-4:] if len(token) > 12 else token}")
    
    # 基础认证测试
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'GitHub-Token-Test/1.0'
    }
    
    print("\n📡 测试 1: 基础认证...")
    try:
        response = requests.get('https://api.github.com/user', headers=headers)
        if response.status_code == 200:
            user_info = response.json()
            print(f"✅ 认证成功! 用户: {user_info.get('login', 'Unknown')}")
            print(f"   账户类型: {user_info.get('type', 'Unknown')}")
        else:
            print(f"❌ 认证失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False
    
    # 测试访问目标仓库
    print("\n📡 测试 2: 访问目标仓库权限...")
    repo_url = 'https://api.github.com/repos/PotatoOfficialTeam/flclash'
    try:
        response = requests.get(repo_url, headers=headers)
        if response.status_code == 200:
            repo_info = response.json()
            print(f"✅ 仓库访问成功!")
            print(f"   仓库名: {repo_info.get('full_name', 'Unknown')}")
            print(f"   是否私有: {repo_info.get('private', False)}")
            print(f"   默认分支: {repo_info.get('default_branch', 'Unknown')}")
        elif response.status_code == 404:
            print("❌ 仓库不存在或无访问权限 (404)")
            return False
        else:
            print(f"❌ 仓库访问失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False
    
    # 测试 Token 权限范围
    print("\n📡 测试 3: 检查 Token 权限范围...")
    if 'X-OAuth-Scopes' in response.headers:
        scopes = response.headers['X-OAuth-Scopes'].split(', ')
        print(f"✅ Token 权限: {', '.join(scopes)}")
        
        required_scopes = ['repo']
        missing_scopes = [scope for scope in required_scopes if scope not in scopes]
        if missing_scopes:
            print(f"⚠️  缺少必要权限: {', '.join(missing_scopes)}")
        else:
            print("✅ 权限充足")
    
    # 生成 Git clone 命令
    print("\n🔧 推荐的 Git clone 命令:")
    print(f"git clone https://x-access-token:{token}@github.com/PotatoOfficialTeam/flclash.git")
    
    return True

if __name__ == "__main__":
    print("🚀 GitHub Token 测试工具")
    print("=" * 50)
    
    success = test_token()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ 所有测试通过!")
    else:
        print("❌ 测试失败，请检查 Token 配置")
        sys.exit(1)