from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from . import views

routers = routers.DefaultRouter()
routers.register(r'client', views.ClientViewSet)
routers.register(r'clientSite', views.ClientSiteViewSet)
routers.register(r'signal', views.SignalViewSet)

urlpatterns = [
    path('', include(routers.urls)),
]