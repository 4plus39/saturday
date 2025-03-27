import datetime
import requests
from typing import List, Dict, Any

def get_next_saturday() -> datetime.datetime:
    """
    計算到下一個星期六的日期
    
    Returns:
        datetime.datetime: 下一個星期六的日期時間
    """
    now = datetime.datetime.now()
    # 計算距離下一個星期六的天數（5代表星期六）
    days_until_saturday = (5 - now.weekday() + 7) % 7
    if days_until_saturday == 0:
        days_until_saturday = 7
    # 設定下一個星期六的日期，並將時間設為當天開始
    next_saturday = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=days_until_saturday)
    return next_saturday

def fetch_weather_data(locations: List[Dict[str, str]], next_saturday: datetime.datetime, api_key: str) -> List[Dict[str, Any]]:
    """
    從氣象局 API 獲取天氣資料
    
    Args:
        locations (List[Dict[str, str]]): 地區資訊列表
        next_saturday (datetime.datetime): 目標日期
        api_key (str): 氣象局 API 金鑰
    
    Returns:
        List[Dict[str, Any]]: 處理後的天氣資料列表
    """
    # 設定查詢時間範圍（從下一個星期六的 00:00 到 18:00）
    time_from = next_saturday.strftime("%Y-%m-%dT00:00:00")
    time_to = next_saturday.strftime("%Y-%m-%dT18:00:00")
    weather_data_list = []

    # 遍歷所有地區，獲取天氣資訊
    for loc in locations:
        # 構建 API 請求 URL
        url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/{loc['resource_id']}?Authorization={api_key}&LocationName={loc['location_name']}&timeFrom={time_from}&timeTo={time_to}"
        try:
            # 發送 API 請求
            response = requests.get(url)
            response.raise_for_status()
            weather_data = response.json()

            # 解析 API 回應的資料結構
            locations_data = weather_data.get("records", {}).get("Locations", [])
            if locations_data:
                location_info = locations_data[0].get("Location", [])
                if location_info:
                    weather_elements = location_info[0].get("WeatherElement", [])
                    
                    # 將天氣資料整理成字典格式
                    weather_info = {}
                    for element in weather_elements:
                        element_name = element.get("ElementName")
                        time_data = element.get("Time", [])
                        weather_info[element_name] = time_data

                    # 加入地區名稱資訊
                    weather_info["地區"] = f"{loc['city']} {loc['location_name']}"
                    weather_data_list.append(weather_info)

        except requests.exceptions.RequestException as e:
            print(f"無法獲取 {loc['city']} {loc['location_name']} 的氣象資訊: {str(e)}")
    
    return weather_data_list 