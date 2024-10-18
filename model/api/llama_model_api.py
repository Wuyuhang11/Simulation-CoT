import requests
import json
import guidance

"""
1.定义函数get_simulation_cot，接受两个参数
- user_question：用户输入的问题
- user_prompt：提示词
"""


def get_simulation_cot_abstraction(user_question, user_prompt):
    # 1.定义 API 请求的 URL 地址
    url = "https://api.siliconflow.cn/v1/chat/completions"
    # 2.创建请求的有效载荷（payload），其中包含模型类型和用户输入的消息
    messages = []
    prompt = ""
    # 如果提供了提示词，就将提示词作为系统消息加入消息列表
    if user_prompt:
        prompt = user_prompt
        messages.append({
            "role": "user",
            "content": prompt
        })
    # 将用户问题加入消息列表

    payload = {
        "math": "Pro/meta-llama/Meta-Llama-3-8B-Instruct",
        "messages": [
            {
                "role": "user",
                "content": user_question  # 将用户输入的问题传递到请求的消息内容中
            }
        ]
    }
    # 3.定义请求的头信息，包括授权信息和内容类型
    headers = {
        "Authorization": "Bearer sk-kifqepgmrmlstabhxlmxrylkppvcppumtvwcdbwajgotuvvk",
        "Content-Type": "application/json"
    }
    # 4.使用 requests 库发送 POST 请求到指定的 URL，传递 payload 和 headers
    response = requests.request("POST", url, json=payload, headers=headers)
    # 5.将返回的 response.text 字符串转换为 JSON 格式，方便后续操作
    response_json = json.loads(response.text)
    # 6.从转换后的 JSON 数据中提取出 'choices' 列表中的第一个元素，并访问 'message' 下的 'content' 字段，获取模型的回复内容
    content = response_json['choices'][0]['message']['content']
    return content


"""
2.得到关系
"""


def get_simulation_cot_relation(user_prompt):
    # 1.定义 API 请求的 URL 地址
    url = "https://api.siliconflow.cn/v1/chat/completions"
    # 2.创建请求的有效载荷（payload），其中包含模型类型和用户输入的消息
    messages = []
    # 如果提供了提示词，就将提示词作为系统消息加入消息列表
    if user_prompt:
        prompt = user_prompt
        messages.append({
            "role": "user",
            "content": prompt
        })
    # 将用户问题加入消息列表

    payload = {
        "model": "Pro/meta-llama/Meta-Llama-3-8B-Instruct",
        "messages": messages  # 消息内容
    }
    # 3.定义请求的头信息，包括授权信息和内容类型
    headers = {
        "Authorization": "Bearer sk-kifqepgmrmlstabhxlmxrylkppvcppumtvwcdbwajgotuvvk",
        "Content-Type": "application/json"
    }
    # 4.使用 requests 库发送 POST 请求到指定的 URL，传递 payload 和 headers
    response = requests.request("POST", url, json=payload, headers=headers)
    # 5.将返回的 response.text 字符串转换为 JSON 格式，方便后续操作
    response_json = json.loads(response.text)
    # 6.从转换后的 JSON 数据中提取出 'choices' 列表中的第一个元素，并访问 'message' 下的 'content' 字段，获取模型的回复内容
    content = response_json['choices'][0]['message']['content']
    return content

"""
3.生成示例example
"""
def get_simulation_cot_example(user_prompt):
    # 1.定义 API 请求的 URL 地址
    url = "https://api.siliconflow.cn/v1/chat/completions"
    # 2.创建请求的有效载荷（payload），其中包含模型类型和用户输入的消息
    messages = []
    # 如果提供了提示词，就将提示词作为系统消息加入消息列表
    if user_prompt:
        prompt = user_prompt
        messages.append({
            "role": "user",
            "content": prompt
        })
    # 将用户问题加入消息列表

    payload = {
        "model": "Pro/meta-llama/Meta-Llama-3-8B-Instruct",
        "messages": messages  # 消息内容
    }
    # 3.定义请求的头信息，包括授权信息和内容类型
    headers = {
        "Authorization": "Bearer sk-kifqepgmrmlstabhxlmxrylkppvcppumtvwcdbwajgotuvvk",
        "Content-Type": "application/json"
    }
    # 4.使用 requests 库发送 POST 请求到指定的 URL，传递 payload 和 headers
    response = requests.request("POST", url, json=payload, headers=headers)
    # 5.将返回的 response.text 字符串转换为 JSON 格式，方便后续操作
    response_json = json.loads(response.text)
    # 6.从转换后的 JSON 数据中提取出 'choices' 列表中的第一个元素，并访问 'message' 下的 'content' 字段，获取模型的回复内容
    content = response_json['choices'][0]['message']['content']
    return content

"""
4.通过滑动窗口的方式产生新的示例
"""
def get_simulation_cot_window(user_prompt):
    # 1.定义 API 请求的 URL 地址
    url = "https://api.siliconflow.cn/v1/chat/completions"
    # 2.创建请求的有效载荷（payload），其中包含模型类型和用户输入的消息
    messages = []
    # 如果提供了提示词，就将提示词作为系统消息加入消息列表
    if user_prompt:
        prompt = user_prompt
        messages.append({
            "role": "user",
            "content": prompt
        })
    # 将用户问题加入消息列表

    payload = {
        "model": "Pro/meta-llama/Meta-Llama-3-8B-Instruct",
        "messages": messages  # 消息内容
    }
    # 3.定义请求的头信息，包括授权信息和内容类型
    headers = {
        "Authorization": "Bearer sk-kifqepgmrmlstabhxlmxrylkppvcppumtvwcdbwajgotuvvk",
        "Content-Type": "application/json"
    }
    # 4.使用 requests 库发送 POST 请求到指定的 URL，传递 payload 和 headers
    response = requests.request("POST", url, json=payload, headers=headers)
    # 5.将返回的 response.text 字符串转换为 JSON 格式，方便后续操作
    response_json = json.loads(response.text)
    # 6.从转换后的 JSON 数据中提取出 'choices' 列表中的第一个元素，并访问 'message' 下的 'content' 字段，获取模型的回复内容
    content = response_json['choices'][0]['message']['content']
    return content


"""
5.给示例和背景集合生成报告
"""
def get_simulation_cot_report(user_prompt):
    # 1.定义 API 请求的 URL 地址
    url = "https://api.siliconflow.cn/v1/chat/completions"
    # 2.创建请求的有效载荷（payload），其中包含模型类型和用户输入的消息
    messages = []
    # 如果提供了提示词，就将提示词作为系统消息加入消息列表
    if user_prompt:
        prompt = user_prompt
        messages.append({
            "role": "user",
            "content": prompt
        })
    # 将用户问题加入消息列表

    payload = {
        "model": "Pro/meta-llama/Meta-Llama-3-8B-Instruct",
        "messages": messages  # 消息内容
    }
    # 3.定义请求的头信息，包括授权信息和内容类型
    headers = {
        "Authorization": "Bearer sk-kifqepgmrmlstabhxlmxrylkppvcppumtvwcdbwajgotuvvk",
        "Content-Type": "application/json"
    }
    # 4.使用 requests 库发送 POST 请求到指定的 URL，传递 payload 和 headers
    response = requests.request("POST", url, json=payload, headers=headers)
    # 5.将返回的 response.text 字符串转换为 JSON 格式，方便后续操作
    response_json = json.loads(response.text)
    # 6.从转换后的 JSON 数据中提取出 'choices' 列表中的第一个元素，并访问 'message' 下的 'content' 字段，获取模型的回复内容
    content = response_json['choices'][0]['message']['content']
    return content


"""
6.生成最终答案
"""
def get_simulation_cot_answer(user_prompt):
    # 1.定义 API 请求的 URL 地址
    url = "https://api.siliconflow.cn/v1/chat/completions"
    # 2.创建请求的有效载荷（payload），其中包含模型类型和用户输入的消息
    messages = []
    # 如果提供了提示词，就将提示词作为系统消息加入消息列表
    if user_prompt:
        prompt = user_prompt
        messages.append({
            "role": "user",
            "content": prompt
        })
    # 将用户问题加入消息列表

    payload = {
        "model": "Pro/meta-llama/Meta-Llama-3-8B-Instruct",
        "messages": messages  # 消息内容
    }
    # 3.定义请求的头信息，包括授权信息和内容类型
    headers = {
        "Authorization": "Bearer sk-kifqepgmrmlstabhxlmxrylkppvcppumtvwcdbwajgotuvvk",
        "Content-Type": "application/json"
    }
    # 4.使用 requests 库发送 POST 请求到指定的 URL，传递 payload 和 headers
    response = requests.request("POST", url, json=payload, headers=headers)
    # 5.将返回的 response.text 字符串转换为 JSON 格式，方便后续操作
    response_json = json.loads(response.text)
    # 6.从转换后的 JSON 数据中提取出 'choices' 列表中的第一个元素，并访问 'message' 下的 'content' 字段，获取模型的回复内容
    content = response_json['choices'][0]['message']['content']
    return content