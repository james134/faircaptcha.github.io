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

class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    
    def create(self, request, *args, **kwargs):
        serializer_class = SiteSerializer(context={'request': request})
        print(request.data)
        query = Site.objects.filter(url=request.data["url"],email=request.data["email"])
        serializer = SiteSerializer(query,many = True, context={"request": request})
        siteT = serializer.data
        print(siteT)
        if siteT==[]:
            site = Site.objects.create(
                url=request.data["url"],
                email= request.data["email"],
                public_key=''.join(random.choices(string.ascii_letters +
                             string.digits, k = 15)),
                secret_key = ''.join(random.choices(string.ascii_letters+
                             string.digits, k = 64))
            )
            signals = (request.data).getlist("signals[]")
            site.signals.set(signals)
            site.save()
            serializer = SiteSerializer(site,context={'request': request})
            return Response({"api_key":serializer.data["public_key"], "secret" : serializer.data["secret_key"]}, status=200)
        else : 
            return Response({"error": "la combinaison email and url existe déjà"}, status=200)

class VisitorViewSet(viewsets.ViewSet):
    serializer_class = VisitorSerializer
    def list(self, request):
        queryset = Site.objects.all()
        site= get_object_or_404(queryset, public_key=request.query_params.get('client'))
        print(site)
        if site is not None :
            if request.query_params.get('type') =="audio":
                token = ''.join(random.choices(string.ascii_letters +
                 string.digits+string.punctuation, k = 15)) 
                visitor =  Visitor.objects.create(
                    ip=request.query_params.get('ip'),
                    token=token,
                    Site = site,
                    score = 0
                )
                visitor.save()
                serializer =  VisitorSerializer(visitor,context={'request': request})
                return render(request, "captcha_audio.html")
            if request.query_params.get('type') =="image": 
                cap = gen_captcha_img()
                token = ''.join(random.choices(string.ascii_letters +
                    string.digits+string.punctuation, k = 15)) 
                visitor =  Visitor.objects.create(
                ip=request.query_params.get('ip'),
                token=token,
                Site = site,
                text = cap["cap_text"],
                score = 0
                )
                visitor.save()
                serializer =  VisitorSerializer(visitor,context={'request': request})
                data = {'url' :"http://127.0.0.1:8000/captcha_img/"+cap["name"]+".png",
                'token' :token,'ip' :request.query_params.get('ip'),'client_key' : request.query_params.get('client')  }
                return render(request,"captcha_image.html",{'data' : data})
        else : 
            return render(request, "")

    def create(self, request, *args, **kwargs):
        print(request.data)
        queryset= Site.objects.all()
        site= get_object_or_404(queryset, public_key= request.data["client_key"])
        print(site)
        if site is not None :
            visitor = Visitor.objects.get(token= request.data["token"],ip=request.data["ip"])
            serializer =  VisitorSerializer(visitor,context={'request': request})
            if(serializer.data["text"] == request.data["text"]):
                visitor.score = 1.0
                visitor.save()
                print("c'est moi le bon")
            return Response({"ip":(serializer.data)['ip'],"token":(serializer.data)['token']}, status=200)
        else : 
            return Response({"error" :"you don't have access"}, status=401)
        
class SignalViewSet(viewsets.ModelViewSet):
    queryset = Signal.objects.all()
    serializer_class = SignalSerializer

@api_view(['POST'])
def getScoreVisitor(request):
    queryset = Site.objects.all()
    site= get_object_or_404(queryset, public_key=request.data['client'], secret_key=request.data['secret_key'])
    print(site)
    if site is not None :
        visitor = Visitor.objects.get(token= request.data["token"],ip=request.data["ip"])
        serializer =  VisitorSerializer(visitor,context={'request': request})
        return Response({"ip":(serializer.data)['ip'],"token":(serializer.data)['token'],"score":(serializer.data)['score']}, status=200)
    else : 
        return Response({"error" :"you don't have access"}, status=401)
