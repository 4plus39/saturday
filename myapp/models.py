from django.db import models


# Create your models here.
# myapp/models.py

class VisitorIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)  # 設定唯一約束
    hostname = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} @ {self.path} - {self.timestamp}"
