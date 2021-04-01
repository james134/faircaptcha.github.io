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
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from django.shortcuts import render
from .gene_image import  gen_captcha_img

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
                             string.digits, k = 15)),
                secret_key = ''.join(random.choices(string.ascii_uppercase +
                             string.digits+string.punctuation, k = 30))
            )
            client.signals.set([3])
            #request.data["signals"]
            client.save()
            serializer = ClientSerializer(client,context={'request': request})
            return Response(serializer.data, status=200)
        else : 
            return Response({"error": "url exist"}, status=200)

class ClientSiteViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Client.objects.all()
        client= get_object_or_404(queryset, public_key=request.query_params.get('client'))
        print(client)
        if client is not None :
            token = ''.join(random.choices(string.ascii_letters +
                    string.digits+string.punctuation, k = 15)) 
            client_site =  ClientSite.objects.create(
                ip=request.query_params.get('ip'),
                token=token,
                client = client,
                score = 0
            )
            client_site.save()
            serializer =  ClientSiteSerializer(client_site,context={'request': request})
            if request.query_params.get('type') =="audio":
                return render(request, "captcha_audio.html")
            if request.query_params.get('type') =="image": 
                data = {'url' :"http://127.0.0.1:8000/captcha_img/"+gen_captcha_img()+".png",
                'token' :token,'ip' :request.query_params.get('ip'),'client_key' : request.query_params.get('client')  }
                return render(request,"captcha_image.html",{'data' : data})
        else : 
            return render(request, "")

    def create(self, request):
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
            return Response({"error" :"you don't have access"}, status=200)
        else : 
            return Response({"error" :"you don't have access"}, status=401)
        

class SignalViewSet(viewsets.ModelViewSet):
    queryset = Signal.objects.all()
    serializer_class = SignalSerializer

""" class CaptchaAudio(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'captcha_audio.html'
    def create (self, request):
        print(1)
        queryset = Client.objects.all()
        client= get_object_or_404(queryset, public_key=request.query_params.get('client'))
        print(client)
        if client is not None :
            return Response({"da":"efe"},status =200)
        else : 
            return Response({"da":"efe"},status =404)

   
 """