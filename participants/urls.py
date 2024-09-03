from django.urls import path
from .views import custom_login, user_dashboard

urlpatterns = [
    path('login/',custom_login,name="login"),
    path('home/',user_dashboard,name="home"),
]