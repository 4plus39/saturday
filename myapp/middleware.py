# myapp/middleware.py
import socket
import requests
from .models import VisitorIP
from django.utils import timezone
import pytz

# 設定台北時間
taipei_tz = pytz.timezone('Asia/Taipei')

class VisitorIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        ip = self.get_client_ip(request)
        path = request.path
        hostname = self.get_hostname(ip)
        location = self.get_location(ip)
        try:
            user_agent = request.user_agent.browser.family + ' on ' + request.user_agent.os.family
        except Exception:
            user_agent = "Unknown"

        # 獲取台北時間
        current_time_taipei = timezone.now().astimezone(taipei_tz)

        # 每次訪問都新增一筆紀錄
        VisitorIP.objects.create(
            ip_address=ip,
            hostname=hostname,
            location=location,
            user_agent=user_agent,
            path=path,
            timestamp=current_time_taipei,
        )

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        return ip.split(':')[0]  # 去掉可能的 port

    def get_hostname(self, ip):
        try:
            return socket.gethostbyaddr(ip)[0]
        except Exception:
            return None

    def get_location(self, ip):
        try:
            response = requests.get(f'https://ipapi.co/{ip}/json/', timeout=2)
            data = response.json()
            country = data.get('country_name')
            city = data.get('city')
            return f"{country}, {city}" if country and city else country or "Unknown"
        except Exception:
            return "Unknown"
