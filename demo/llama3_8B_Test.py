import requests

url = "https://api.siliconflow.cn/v1/chat/completions"

payload = {
    "model": "Pro/meta-llama/Meta-Llama-3-8B-Instruct",
    "messages": [
        {
            "role": "user",
            "content": "你是谁？讲出你的配置"
        }
    ]
}
headers = {
    "Authorization": "Bearer sk-kifqepgmrmlstabhxlmxrylkppvcppumtvwcdbwajgotuvvk",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)