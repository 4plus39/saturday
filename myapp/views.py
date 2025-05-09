from django.shortcuts import render
from .utils import fetch_weather_data, get_next_saturday
from django.conf import settings
from .models import VisitorIP
import pytz



# 定義要查詢的地區資訊，包含資源ID、地區名稱和城市名稱
LOCATIONS = [
    {"resource_id": "F-D0047-063", "location_name": "中正區", "city": "臺北市"},
    {"resource_id": "F-D0047-071", "location_name": "板橋區", "city": "新北市"},
    {"resource_id": "F-D0047-007", "location_name": "中壢區", "city": "桃園市"},
    {"resource_id": "F-D0047-055", "location_name": "東區", "city": "新竹市"},
    {"resource_id": "F-D0047-015", "location_name": "頭份市", "city": "苗栗縣"},
]

def combined_view(request):
    """
    組合視圖：顯示倒數計時和天氣預報
    使用 settings.py 中的 API key
    """
    # 獲取下一個星期六的日期
    next_saturday = get_next_saturday()
    
    # 獲取天氣資料
    weather_data_list = fetch_weather_data(LOCATIONS, next_saturday, settings.CWA_API_KEY)

    # 設定台北時區
    taipei_tz = pytz.timezone('Asia/Taipei')

    # 取得最新的五筆資料（timestamp 降冪排序）
    visitors = VisitorIP.objects.order_by('-timestamp')[:5]
    
    # 將每一筆的 timestamp 轉換成台北時間
    for visitor in visitors:
        visitor.timestamp = visitor.timestamp.astimezone(taipei_tz)
    
    # 準備傳遞給模板的資料
    context = {
        "next_saturday": next_saturday.isoformat(),
        "weather_data_list": weather_data_list,
        "target_date": next_saturday.strftime("%Y/%m/%d"),
        "visitors": visitors,  # 用上面排好、只取5筆的 visitors
    }
    
    return render(request, "combined.html", context)