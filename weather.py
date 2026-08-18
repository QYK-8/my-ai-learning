import requests

# 让用户输入经纬度
lat = input("请输入纬度（如 39.9）: ")
lon = input("请输入经度（如 116.4）: ")

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": float(lat),
    "longitude": float(lon),
    "current_weather": True
}

response = requests.get(url, params=params)
data = response.json()
current = data["current_weather"]

print(f"温度: {current['temperature']}°C")