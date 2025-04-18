"""
URL configuration for keister_house project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

admin.site.site_header = "Biddify Admin"
admin.site.site_title = "Biddify Admin Portal"
admin.site.index_title = "Welcome to the Admin Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("participants.urls")),
    path("items/", include("item.urls")),
    path("auction/", include("bid.urls")),
    path("payment/", include("payments.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path('admin_tools_stats/', include('admin_tools_stats.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
