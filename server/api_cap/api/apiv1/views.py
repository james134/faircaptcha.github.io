from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import *
from .serializers import *
import requests
import string
import random


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    def create(self, request, *args, **kwargs):
        serializer_class = ClientSerializer(context={'request': request})
        print(request.data)
        query = Client.objects.filter(url=request.data["url"])
        serializer = ClientSerializer(query,many = True, context={"request": request})
        clientT = serializer.data
        print(clientT)
        print (2)
        if clientT==[]:
            print (3)
            client = Client.objects.create(
                url=request.data["url"],
                public_key=''.join(random.choices(string.ascii_letters +
                             string.digits+string.punctuation, k = 15)),
                secret_key = ''.join(random.choices(string.ascii_uppercase +
                             string.digits+string.punctuation, k = 30))
            )
            client.signals.set(request.data["signals"])
            client.save()
            serializer = ClientSerializer(client,context={'request': request})
            return Response(serializer.data, status=200)
        else : 
            return Response({"error": "url exist"}, status=200)

class ClientSiteViewSet(viewsets.ModelViewSet):
    queryset =  ClientSite.objects.all()
    serializer_class =  ClientSiteSerializer
    def create(self, request, *args, **kwargs):
        print(request.data)
        queryset= Client.objects.all()
        client= get_object_or_404(queryset, public_key= request.data["client"])
        print(client)
        if client is not None :
            token = ''.join(random.choices(string.ascii_letters +
                                string.digits+string.punctuation, k = 15)) 
            client_site =  ClientSite.objects.create(
                ip=request.data["ip"],
                token=token,
                client = client,
                score = 0
            )
            client_site.save()
            serializer =  ClientSiteSerializer(client_site,context={'request': request})
            return Response(serializer.data, status=200)
        else : 
            Response({"error" :"you don't have access"}, status=401)
        

class SignalViewSet(viewsets.ModelViewSet):
    queryset = Signal.objects.all()
    serializer_class = SignalSerializer