from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from . import views

routers = routers.DefaultRouter()
routers.register(r'client', views.SiteViewSet)
routers.register(r'clientSite', views.VisitorViewSet, basename= "clientSite")
routers.register(r'signal', views.SignalViewSet)

urlpatterns = [
    path('', include(routers.urls)),
    path('getScore/', views.getScoreVisitor)
]