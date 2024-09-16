from django.urls import path
from .views import custom_login, user_dashboard, user_register

urlpatterns = [
    path('login/',custom_login,name="login"),
    path('home/',user_dashboard,name="home"),
    path('register/',user_register,name="user_register")
]