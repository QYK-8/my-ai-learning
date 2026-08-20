# Open-Meteo 实时天气 API 调用文档

## 1. 接口概述

| 项目 | 内容 |
|------|------|
| **接口名称** | 实时天气查询 |
| **接口描述** | 获取指定经纬度位置的当前天气数据 |
| **请求方式** | GET |
| **请求地址** | `https://api.open-meteo.com/v1/forecast` |
| **认证方式** | 无需认证（免费开源） |

---

## 2. 请求参数

| 参数名 | 类型 | 必选 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `latitude` | float | ✅ 是 | 纬度（范围 -90 到 90） | `39.9` |
| `longitude` | float | ✅ 是 | 经度（范围 -180 到 180） | `116.4` |
| `current_weather` | bool | ❌ 否 | 是否返回当前天气，`true` 或 `false` | `true` |

---

## 3. 请求示例

### Python 示例

```python
import requests

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 39.9,
    "longitude": 116.4,
    "current_weather": True
}

response = requests.get(url, params=params)
data = response.json()
temperature = data["current_weather"]["temperature"]
```

### 请求 URL 示例

```
https://api.open-meteo.com/v1/forecast?latitude=39.9&longitude=116.4&current_weather=true
```

---

## 4. 返回数据字段说明

| 字段名 | 类型 | 单位 | 说明 |
|--------|------|------|------|
| `latitude` | float | - | 请求的纬度 |
| `longitude` | float | - | 请求的经度 |
| `timezone` | string | - | 时区 |
| `current_weather.temperature` | float | °C | 当前温度 |
| `current_weather.windspeed` | float | km/h | 当前风速 |
| `current_weather.winddirection` | float | ° | 当前风向（角度） |
| `current_weather.weathercode` | int | - | 天气状况代码 |
| `current_weather.time` | string | - | 数据时间 |

---

## 5. 返回示例

```json
{
  "latitude": 39.9,
  "longitude": 116.4,
  "timezone": "GMT",
  "current_weather": {
    "temperature": 26.5,
    "windspeed": 15.3,
    "winddirection": 120,
    "weathercode": 1,
    "time": "2026-08-18T15:00"
  }
}
```

---

## 6. 测试结果

| 城市 | 坐标 | 测试时间 | 温度 |
|------|------|----------|------|
| 北京 | 39.9, 116.4 | 2026-08-18 | 26.5°C |

**文档版本**：v1.0  
**最后更新**：2026-08-18