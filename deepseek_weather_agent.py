import requests
from openai import OpenAI

# ========== 1. 配置区 ==========
API_KEY = ""  # 替换成你的 DeepSeek Key
client = OpenAI(api_key="", base_url="https://api.deepseek.com/v1")


# ========== 2. 真实的后端函数（查天气的代码） ==========
def get_weather_desc(code):
    weather_map = {0: ("☀️", "晴天"), 1: ("🌤️", "少云"), 3: ("☁️", "阴天"), 61: ("🌦️", "小雨"), 95: ("⛈️", "雷暴")}
    return weather_map.get(code, ("🌈", "未知"))


def get_real_weather(city_name):
    """这个函数会真正去网上查天气，返回字符串结果"""
    try:
        # 城市转经纬度
        geo_resp = requests.get("https://geocoding-api.open-meteo.com/v1/search",
                                params={"name": city_name, "count": 1})
        geo_data = geo_resp.json()
        if not geo_data.get("results"):
            return f"未找到城市：{city_name}"

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        found_city = geo_data["results"][0]["name"]

        # 查天气
        weather_resp = requests.get("https://api.open-meteo.com/v1/forecast",
                                    params={"latitude": lat, "longitude": lon, "current_weather": True})
        current = weather_resp.json()["current_weather"]
        emoji, desc = get_weather_desc(current["weathercode"])

        return f"{found_city}天气：{emoji}{desc}，温度{current['temperature']}°C，风速{current['windspeed']}km/h"
    except Exception as e:
        return f"查天气出错了：{str(e)}"


# ========== 3. 告诉 AI 它有这个工具可用（Function Calling 核心） ==========
tools = [{
    "type": "function",
    "function": {
        "name": "get_real_weather",
        "description": "查询指定城市的实时天气情况",
        "parameters": {
            "type": "object",
            "properties": {
                "city_name": {"type": "string", "description": "城市名称，比如：北京、上海"}
            },
            "required": ["city_name"]
        }
    }
}]

# ========== 4. 开始多轮对话（带工具调用） ==========
print("🤖 AI 天气助手已启动（输入 exit 退出）")
messages = [{"role": "system", "content": "你是一个天气助手，当用户问天气时调用工具，并依据工具结果用中文回答。"}]

while True:
    user_input = input("\n👤 你: ")
    if user_input.lower() in ["exit", "退出"]:
        print("👋 再见！")
        break

    # 把用户问题加入历史
    messages.append({"role": "user", "content": user_input})

    # 第一次请求：让 AI 判断是否需要调用工具
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools,  # 把工具描述传给 AI
        tool_choice="auto"  # 让 AI 自己决定要不要用
    )

    response_message = response.choices[0].message

    # 检查 AI 是否要求调用工具
    if response_message.tool_calls:
        tool_call = response_message.tool_calls[0]
        # 解析 AI 提取的城市名
        import json

        args = json.loads(tool_call.function.arguments)
        city = args.get("city_name")

        print(f"🔧 [AI 正在调用天气工具查询：{city}...]")

        # 执行真正的查天气函数
        weather_result = get_real_weather(city)

        # 把工具返回的结果喂回给 AI
        messages.append(response_message)  # AI 的“我要调用工具”指令
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": weather_result
        })

        # 第二次请求：让 AI 根据工具返回的真实数据，生成最终回复
        second_response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )
        final_reply = second_response.choices[0].message.content
        print(f"🤖 AI: {final_reply}")
        messages.append({"role": "assistant", "content": final_reply})
    else:
        # 如果没有调用工具，直接输出回复
        print(f"🤖 AI: {response_message.content}")
        messages.append({"role": "assistant", "content": response_message.content})