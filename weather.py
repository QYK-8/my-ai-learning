import requests

def get_weather_desc(code):
    """将天气代码转成中文描述和 emoji"""
    weather_map = {
        0: ("☀️", "晴天"),
        1: ("🌤️", "少云"),
        2: ("⛅", "多云"),
        3: ("☁️", "阴天"),
        45: ("🌫️", "雾"),
        48: ("🌫️", "霜雾"),
        51: ("🌧️", "小毛毛雨"),
        53: ("🌧️", "毛毛雨"),
        55: ("🌧️", "大毛毛雨"),
        61: ("🌦️", "小雨"),
        63: ("🌧️", "中雨"),
        65: ("🌧️", "大雨"),
        71: ("❄️", "小雪"),
        73: ("❄️", "中雪"),
        75: ("❄️", "大雪"),
        80: ("🌧️", "阵雨"),
        81: ("🌧️", "中阵雨"),
        82: ("⛈️", "大阵雨"),
        95: ("⛈️", "雷暴"),
        96: ("⛈️", "雷暴加冰雹"),
        99: ("⛈️", "强雷暴加冰雹"),
    }
    return weather_map.get(code, ("🌈", "未知天气"))

# ========== 主程序 ==========
city = input("请输入城市名称（如：北京、上海、广州）: ")

# 城市名 → 经纬度
geo_url = "https://geocoding-api.open-meteo.com/v1/search"
geo_response = requests.get(geo_url, params={"name": city, "count": 1, "language": "zh"})
geo_data = geo_response.json()

if not geo_data.get("results"):
    print(f"❌ 未找到城市: {city}")
else:
    lat = geo_data["results"][0]["latitude"]
    lon = geo_data["results"][0]["longitude"]
    found_city = geo_data["results"][0]["name"]
    country = geo_data["results"][0].get("country", "")
    timezone = geo_data["results"][0].get("timezone", "UTC")

    # 经纬度 → 天气
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    }
    weather_response = requests.get(weather_url, params=weather_params)
    weather_data = weather_response.json()
    current = weather_data["current_weather"]

    # 翻译天气代码
    emoji, desc = get_weather_desc(current["weathercode"])

    # 美化输出
    print("\n" + "=" * 40)
    print(f"  📍 {found_city}，{country}")
    print("=" * 40)
    print(f"  {emoji}  {desc}")
    print(f"  🌡️  温度：{current['temperature']}°C")
    print(f"  💨  风速：{current['windspeed']} km/h")
    print(f"  🧭  风向：{current['winddirection']}°")
    print("=" * 40)