import requests
import datetime
from django.shortcuts import render
from django.http import HttpResponse

def combined_view(request):
    # 倒數到下一個星期六的邏輯
    def get_next_saturday():
        now = datetime.datetime.now()
        days_until_saturday = (5 - now.weekday() + 7) % 7
        if days_until_saturday == 0:
            days_until_saturday = 7
        next_saturday = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=days_until_saturday)
        return next_saturday

    next_saturday = get_next_saturday()

    # 定義三個地區的 API 資訊
    locations = [
        {"resource_id": "F-D0047-063", "location_name": "中正區", "city": "臺北市"},
        {"resource_id": "F-D0047-071", "location_name": "板橋區", "city": "新北市"},
        {"resource_id": "F-D0047-007", "location_name": "中壢區", "city": "桃園市"},
        {"resource_id": "F-D0047-055", "location_name": "東區", "city": "新竹市"},
        {"resource_id": "F-D0047-015", "location_name": "頭份市", "city": "苗栗縣"},
        
    ]

    api_key = "CWA-C8895C3C-29ED-40AF-B3A1-0AC72BB0E2CA"
    time_from = next_saturday.strftime("%Y-%m-%dT00:00:00")
    time_to = next_saturday.strftime("%Y-%m-%dT18:00:00")
    weather_data_list = []

    for loc in locations:
        url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/{loc['resource_id']}?Authorization={api_key}&LocationName={loc['location_name']}&timeFrom={time_from}&timeTo={time_to}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # 檢查請求是否成功
            weather_data = response.json()  # 獲取 API 回應的 JSON 資料

            # 提取需要的氣象資料
            locations_data = weather_data.get("records", {}).get("Locations", [])
            if locations_data:
                location_info = locations_data[0].get("Location", [])
                if location_info:
                    weather_elements = location_info[0].get("WeatherElement", [])
                    
                    # 將資料整理成字典，方便傳遞到模板
                    weather_info = {}
                    for element in weather_elements:
                        element_name = element.get("ElementName")
                        time_data = element.get("Time", [])
                        weather_info[element_name] = time_data

                    # 將地區名稱加入資料中
                    weather_info["地區"] = f"{loc['city']} {loc['location_name']}"
                    weather_data_list.append(weather_info)

                    print(f"12小時降雨機率資料片段（{loc['city']} {loc['location_name']}）：")
                    print(weather_info.get("12小時降雨機率", []))
                    print("-" * 50)  # 分隔線

        except requests.exceptions.RequestException as e:
            print(f"無法獲取 {loc['city']} {loc['location_name']} 的氣象資訊: {str(e)}")
        

    
    # 將倒數計時和天氣資料傳遞到模板
    context = {
        "next_saturday": next_saturday.isoformat(),
        "weather_data_list": weather_data_list,
        "target_date": next_saturday.strftime("%Y/%m/%d"),  # 將日期格式化為 YYYY-MM-DD
    }
    print("weather_data_list: ", weather_data_list)

    return render(request, "combined.html", context)