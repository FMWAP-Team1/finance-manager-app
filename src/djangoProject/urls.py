"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

# 임시용 View

# views.py

from django.conf import settings
from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {
        'kakao_javascript_key': settings.KAKAO_JAVASCRIPT_KEY  # .env에서 불러온 키 전달
    })


urlpatterns = [
    path("", index),
    path('admin/', admin.site.urls),
    path("api/user/", include("users.urls")),
    path('', include('transaction_history.urls')),
]
