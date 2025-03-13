from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('countdown/', views.countdown_to_saturday, name='countdown'),
]