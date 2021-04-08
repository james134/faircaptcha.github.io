from django.contrib import admin
from .models import *

@admin.register(Signal)
class SignalAdmin(admin.ModelAdmin):
    list_display = ['name','description', 'created', 'modified']

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['url', 'email','public_key', 'secret_key', 'created','modified']

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['token', 'ip', 'score','text', 'site','created','modified']


# Register your models here.
