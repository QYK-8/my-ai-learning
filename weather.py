import requests

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 39.9,
    "longitude": 116.4,
    "current_weather": True
}

response = requests.get(url, params=params)
data = response.json()

print(f"北京当前温度: {data['current_weather']['temperature']}°C")
