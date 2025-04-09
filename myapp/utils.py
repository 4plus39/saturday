import datetime
import requests
from typing import List, Dict, Any
import json
import os

# 緩存相關常數
CACHE_DIR = "cache"
WEATHER_CACHE_FILE = os.path.join(CACHE_DIR, "weather_cache.json")
CACHE_DURATION = datetime.timedelta(hours=1)  # 緩存有效期為1小時

def convert_wind_speed_to_description(wind_speed):
    """
    將風速(m/s)轉換為葡式風級的中文描述
    """
    try:
        wind_speed = float(wind_speed)
        if wind_speed < 0.3:
            return "無風"
        elif wind_speed < 1.6:
            return "軟風"
        elif wind_speed < 3.4:
            return "輕風"
        elif wind_speed < 5.5:
            return "微風"
        elif wind_speed < 8.0:
            return "和風"
        elif wind_speed < 10.8:
            return "清風"
        elif wind_speed < 13.9:
            return "強風"
        elif wind_speed < 17.2:
            return "疾風"
        elif wind_speed < 20.8:
            return "大風"
        elif wind_speed < 24.5:
            return "烈風"
        elif wind_speed < 28.5:
            return "狂風"
        elif wind_speed < 32.7:
            return "暴風"
        else:
            return "颶風"
    except (ValueError, TypeError):
        return "無風"

def ensure_cache_dir():
    """確保緩存目錄存在"""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

def load_weather_cache() -> Dict[str, Any]:
    """載入天氣資料緩存"""
    ensure_cache_dir()
    if os.path.exists(WEATHER_CACHE_FILE):
        try:
            with open(WEATHER_CACHE_FILE, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                # 檢查緩存是否過期
                cache_time = datetime.datetime.fromisoformat(cache_data['timestamp'])
                if datetime.datetime.now() - cache_time < CACHE_DURATION:
                    return cache_data['data']
        except Exception as e:
            print(f"讀取緩存時發生錯誤: {str(e)}")
    return None

def save_weather_cache(data: List[Dict[str, Any]]):
    """保存天氣資料到緩存"""
    ensure_cache_dir()
    cache_data = {
        'timestamp': datetime.datetime.now().isoformat(),
        'data': data
    }
    try:
        with open(WEATHER_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存緩存時發生錯誤: {str(e)}")

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

def process_wind_data(weather_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    處理天氣資料中的風速資訊，添加風力描述
    
    Args:
        weather_info (Dict[str, Any]): 天氣資訊字典
    
    Returns:
        Dict[str, Any]: 處理後的天氣資訊字典
    """
    if "風速" in weather_info:
        print(f"處理風速數據: {weather_info['風速']}")  # 調試信息
        for wind_data in weather_info["風速"]:
            if "ElementValue" in wind_data and len(wind_data["ElementValue"]) > 0:
                # 檢查 ElementValue 的結構
                print(f"ElementValue 結構: {wind_data['ElementValue']}")
                
                # 獲取風速值
                wind_speed = wind_data["ElementValue"][0].get("WindSpeed")
                print(f"風速值: {wind_speed}")  # 調試信息
                
                if wind_speed is not None:
                    try:
                        # 確保風速值是浮點數
                        wind_speed = float(wind_speed)
                        wind_description = convert_wind_speed_to_description(wind_speed)
                        print(f"風力描述: {wind_description}")  # 調試信息
                        
                        # 添加風力描述到數據中
                        if "ElementValue" in wind_data and len(wind_data["ElementValue"]) > 0:
                            wind_data["ElementValue"][0]["WindDescription"] = wind_description
                            print(f"更新後的 ElementValue: {wind_data['ElementValue']}")  # 調試信息
                    except (ValueError, TypeError) as e:
                        print(f"轉換風速時發生錯誤: {str(e)}")
                        wind_data["ElementValue"][0]["WindDescription"] = "無風"
    return weather_info

def fetch_weather_data(locations: List[Dict[str, str]], next_saturday: datetime.datetime, api_key: str) -> List[Dict[str, Any]]:
    """
    從氣象局 API 獲取天氣資料，優先使用緩存
    
    Args:
        locations (List[Dict[str, str]]): 地區資訊列表
        next_saturday (datetime.datetime): 目標日期
        api_key (str): 氣象局 API 金鑰
    
    Returns:
        List[Dict[str, Any]]: 處理後的天氣資料列表
    """
    # 嘗試從緩存獲取資料
    cached_data = load_weather_cache()
    if cached_data is not None:
        print("使用緩存的天氣資料")
        # 處理緩存中的風速數據
        processed_data = []
        for weather_info in cached_data:
            processed_data.append(process_wind_data(weather_info))
        return processed_data
    
    print("緩存不存在或已過期，從 API 獲取新資料")
    
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
                        print(f"天氣元素: {element_name}, 數據: {time_data}")  # 調試信息

                    # 加入地區名稱資訊
                    weather_info["地區"] = f"{loc['city']} {loc['location_name']}"
                    
                    # 處理風速資料
                    weather_info = process_wind_data(weather_info)
                    
                    weather_data_list.append(weather_info)

        except requests.exceptions.RequestException as e:
            print(f"無法獲取 {loc['city']} {loc['location_name']} 的氣象資訊: {str(e)}")
    
    # 保存到緩存
    if weather_data_list:
        save_weather_cache(weather_data_list)
    
    return weather_data_list 