from django.urls import path
from . import views

urlpatterns = [
    path('', views.combined_view, name='combined_view'),  # 綁定到 /combined/ 路徑
    path('combined/', views.combined_view, name='combined_view'),  # 綁定到 /combined/ 路徑
]