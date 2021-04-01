from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from . import views

routers = routers.DefaultRouter()
routers.register(r'client', views.ClientViewSet)
routers.register(r'clientSite', views.ClientSiteViewSet, basename= "clientSite")
routers.register(r'signal', views.SignalViewSet)
""" routers.register(r'captcha_audio', views.CaptchaAudio.as_view(),basename= "audio") """

urlpatterns = [
    path('', include(routers.urls)),
]