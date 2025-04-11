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

        # 檢查是否已經有相同 IP 的資料
        visitor, created = VisitorIP.objects.update_or_create(
            ip_address=ip,  # 根據 IP 查詢
            defaults={
                'hostname': hostname,
                'location': location,
                'user_agent': user_agent,
                'path': path,
                'timestamp': current_time_taipei,  # 使用台北時間
            }
        )

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # 如果帶有 port，就把它去掉
        return ip.split(':')[0]

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
