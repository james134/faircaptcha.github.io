from .models import *
from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

class SiteSerializer(serializers.ModelSerializer):
    signals = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    public_key = serializers.CharField(
        max_length=68, read_only=True)
    secret_key = serializers.CharField(
        max_length=68, read_only=True)
    class Meta:
        model = Site
        fields = [
            'id',
            'url',
            'public_key',
            'secret_key',
            'signals',
            'created',
            'modified'
        ]


class VisitorSerializer(serializers.HyperlinkedModelSerializer):
    token = serializers.CharField(
        max_length=68, read_only=True)
    text = serializers.CharField(
        max_length=68, read_only=True)
    score = serializers.CharField(
        max_length=68, read_only=True)
    audio = serializers.FileField(
        max_length=68, read_only=True)
    class Meta:
        model = Visitor
        fields = [
            'ip',
            'token',
            'site',
            'score',
            'text',
            'audio',
            'cookie',
            'created',
            'modified'
        ]


class SignalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Signal
        fields = [
            'name',
            'description',
            'created',
            'modified'
        ]

class PhrasesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Phrases
        fields = [
            'id',
            'intitule',
        ]
