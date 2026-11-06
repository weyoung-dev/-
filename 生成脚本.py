
import os
import sys
import requests

# 建议通过环境变量传入，不要硬编码在代码里
API_KEY = os.environ.get("OPENROUTER_API_KEY")

if not API_KEY:
    print("❌ 错误：未找到环境变量 OPENROUTER_API_KEY")
    print("请先设置环境变量，例如：export OPENROUTER_API_KEY='sk-or-v1-...'")
    sys.exit(1)

URL = "https://openrouter.ai/api/v1/chat/completions"

# 使用一个便宜或免费的模型进行测试，避免产生不必要费用
# 你也可以换成 "openai/gpt-4o-mini" 或其他模型
MODEL_ID = "openrouter/free"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

payload = {
    "model": MODEL_ID,
    "messages": [
        {"role": "user", "content": "只回复两个字：正常"}
    ],
    "max_tokens": 10,
}

print(f"正在测试 OpenRouter 连通性...")
print(f"模型: {MODEL_ID}")
print(f"端点: {URL}\n")

try:
    response = requests.post(URL, headers=headers, json=payload, timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ 连通性正常！")
        print("完整响应：")
        import json
        print(json.dumps(data, ensure_ascii=False, indent=2))
        
    elif response.status_code == 401:
        print("❌ 认证失败 (401)：API Key 无效或已过期。")
        print("   请检查你的 Key 是否填写正确，或前往 OpenRouter 后台重新生成。")
        
    elif response.status_code == 402:
        print("❌ 余额不足 (402)：账户额度已用完。")
        print("   请前往 OpenRouter 充值后再试。")
        
    elif response.status_code == 429:
        print("❌ 请求过多 (429)：触发了速率限制。")
        print("   请稍后重试，或检查免费模型的每日/每分钟限额。")
        
    else:
        print(f"❌ 请求失败，状态码: {response.status_code}")
        print(f"   响应内容: {response.text}")

except requests.exceptions.Timeout:
    print("❌ 连接超时：网络无法在规定时间内到达 OpenRouter。")
    print("   请检查网络连接或代理设置。")
except requests.exceptions.ConnectionError:
    print("❌ 连接错误：无法建立网络连接。")
    print("   请检查 DNS 或防火墙设置。")
except Exception as e:
    print(f"❌ 发生未知错误: {e}")