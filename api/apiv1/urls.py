from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from . import views

routers = routers.DefaultRouter()
routers.register(r'site', views.SiteViewSet)
routers.register(r'clientSite', views.VisitorViewSet, basename= "clientSite")
routers.register(r'signal', views.SignalViewSet)
routers.register(r'phrases', views.PhrasesViewSet)

urlpatterns = [
    path('', include(routers.urls)),
    path('getScore/', views.getScoreVisitor),
    path('getStart/', views.getStart),
    path('getFirstScore/', views.getFirstScore),
    path('getNewPhrase/', views.getNewPhrase),
    path('getCookie/', views.getCookie),
    path('getCookieData/', views.getCookieData),
]