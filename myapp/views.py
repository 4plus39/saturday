from django.shortcuts import render
from django.http import HttpResponse
import datetime

def countdown_to_saturday(request):
    def get_next_saturday():
        now = datetime.datetime.now()
        days_until_saturday = (5 - now.weekday() + 7) % 7
        if days_until_saturday == 0:
            days_until_saturday = 7
        next_saturday = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=days_until_saturday)
        return next_saturday

    next_saturday = get_next_saturday()

    # 返回包含 JavaScript 的 HTML 頁面
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>倒數到下一個星期六</title>
        <script>
            function updateCountdown() {{
                // 計算倒數時間
                const nextSaturday = new Date("{next_saturday.isoformat()}");
                const now = new Date();
                const timeDifference = nextSaturday - now;

                // 計算天、時、分、秒
                const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
                const hours = Math.floor((timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);

                // 更新頁面內容
                document.getElementById("countdown").innerHTML = 
                    "距離星期六還有: " + days + "天 " + 
                    String(hours).padStart(2, '0') + "時 " + 
                    String(minutes).padStart(2, '0') + "分 " + 
                    String(seconds).padStart(2, '0') + "秒";
            }}

            // 每秒更新一次
            setInterval(updateCountdown, 1000);

            // 頁面加載時立即更新
            window.onload = updateCountdown;
        </script>
    </head>
    <body>
        <h1 id="countdown">載入中...</h1>
    </body>
    </html>
    """
    return HttpResponse(html)
    
def home(request):
    return HttpResponse("Hello, Django!")
    
    