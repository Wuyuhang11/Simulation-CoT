import requests
import copy
import time
import json
import collections
import asyncio


class LLAMA3_8B_Model:
    llm_name: str = "llama3_8b"

    def __init__(self, api_url, api_key, model_name="Pro/meta-llama/Meta-Llama-3-8B-Instruct", caching=True,
                 max_retries=5, max_calls_per_min=60):
        self.api_url = api_url
        self.api_key = api_key
        self.model_name = model_name
        self.caching = caching
        self.max_retries = max_retries
        self.max_calls_per_min = max_calls_per_min
        self.call_history = collections.deque()
        self.cache = {}  # 简单缓存
        self.temperature = 0.7  # 默认值
        self.top_p = 0.9  # 默认值

    def add_call(self):
        """ 添加调用时间戳 """
        now = time.time()
        self.call_history.append(now)

    def count_calls(self):
        """ 统计最近60秒内的调用次数 """
        now = time.time()
        while self.call_history and self.call_history[0] < now - 60:
            self.call_history.popleft()
        return len(self.call_history)

    def prompt_to_messages(self, prompt):
        """ 转换输入 prompt 为 API 所需的 messages 格式 """
        return [{"role": "user", "content": prompt}]

    async def _make_request(self, prompt, max_tokens=512, stop=None, temperature=None, top_p=None, stream=False):
        """ 向 API 发送请求 """
        payload = {
            "math": self.model_name,
            "messages": self.prompt_to_messages(prompt),
            "max_tokens": max_tokens,
            "temperature": temperature if temperature is not None else self.temperature,
            "top_p": top_p if top_p is not None else self.top_p,
            "stream": stream
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.api_key}"
        }

        # 发送请求到 LLaMA API
        response = requests.post(self.api_url, json=payload, headers=headers)
        response.raise_for_status()  # 如果请求失败，抛出异常

        return response.json()

    async def _retry_request(self, prompt, max_tokens=512, stop=None, temperature=None, top_p=None, stream=False):
        """ 支持重试机制的请求 """
        fail_count = 0
        while fail_count < self.max_retries:
            try:
                return await self._make_request(prompt, max_tokens, stop, temperature, top_p, stream)
            except requests.exceptions.RequestException as e:
                fail_count += 1
                if fail_count >= self.max_retries:
                    raise Exception(f"超过最大重试次数: {self.max_retries}. 错误: {str(e)}")
                await asyncio.sleep(3)  # 等待 3 秒后重试

    async def __call__(self, prompt, max_tokens=512, stop=None, temperature=None, top_p=None, stream=False):
        """ 调用接口生成响应 """

        # 确保不超过速率限制
        while self.count_calls() >= self.max_calls_per_min:
            await asyncio.sleep(1)

        cache_key = f"{prompt}-{max_tokens}-{temperature}-{top_p}"

        # 检查缓存
        if cache_key in self.cache and self.caching:
            return self.cache[cache_key]

        # 调用 API 生成响应
        result = await self._retry_request(prompt, max_tokens, stop, temperature, top_p, stream)

        # 缓存结果
        if self.caching:
            self.cache[cache_key] = result

        self.add_call()

        return result


# 使用方式
llama_model = LLAMA3_8B_Model(
    api_url="https://api.siliconflow.cn/v1/chat/completions",
    api_key="sk-kifqepgmrmlstabhxlmxrylkppvcppumtvwcdbwajgotuvvk"
)


# 异步调用模型
async def generate_response():
    result = await llama_model("What is the capital of France?", max_tokens=50)
    print(result)

# 在适当的事件循环中运行 generate_response()
