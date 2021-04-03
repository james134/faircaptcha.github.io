from django.contrib import admin
from .models import *

@admin.register(Signal)
class SignalAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'modified']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['url', 'public_key', 'secret_key', 'created','modified']

@admin.register(ClientSite)
class ClientSiteAdmin(admin.ModelAdmin):
    list_display = ['token', 'ip', 'score','text', 'client','created','modified']


# Register your models here.
