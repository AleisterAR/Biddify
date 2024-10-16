from django.urls import path
from .views import custom_login, user_dashboard, user_register, user_logout, check_username

urlpatterns = [
    path('login/',custom_login,name="login"),
    path('home/',user_dashboard,name="home"),
    path('register/',user_register,name="user_register"),
    path('logout/', user_logout, name="logout")
]

htmx_urlpatterns = [
    path('check_username/',check_username, name="check_username"),
]

urlpatterns += htmx_urlpatterns