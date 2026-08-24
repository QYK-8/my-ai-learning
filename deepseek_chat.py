from openai import OpenAI

API_KEY = "API_KEY"   # 替换成真的

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.deepseek.com/v1"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个有趣的AI助手"},
        {"role": "user", "content": "写一首关于秋天的短诗"}
    ],
    stream=True   # 关键改动
)

for chunk in response:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)