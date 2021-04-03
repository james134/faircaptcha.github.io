from .models import *
from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

class ClientSerializer(serializers.HyperlinkedModelSerializer):
    public_key = serializers.CharField(
        max_length=68, read_only=True)
    secret_key = serializers.CharField(
        max_length=68, read_only=True)
    class Meta:
        model = Client
        fields = [
            'id',
            'url',
            'public_key',
            'secret_key',
            'signals',
            'created',
            'modified'
        ]


class ClientSiteSerializer(serializers.HyperlinkedModelSerializer):
    token = serializers.CharField(
        max_length=68, read_only=True)
    text = serializers.CharField(
        max_length=68, read_only=True)
    score = serializers.CharField(
        max_length=68, read_only=True)
    class Meta:
        model = ClientSite
        fields = [
            'ip',
            'token',
            'client',
            'score',
            'text',
            'created',
            'modified'
        ]


class SignalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Signal
        fields = [
            'name',
            'created',
            'modified'
        ]
