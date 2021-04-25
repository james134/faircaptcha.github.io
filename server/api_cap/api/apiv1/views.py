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
from difflib import SequenceMatcher

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
        print(request.data)
        site= get_object_or_404(queryset, public_key=request.query_params.get('client_key'))
        print(site)
        if site is not None :
            print("t1")
            if request.query_params.get('type') =="audio":
                print("t2")
                idPhrase = "en"+str(random.randint(1, 2))
                phrase = Phrases.objects.get(id= idPhrase)
                serializer =  PhrasesSerializer(phrase,context={'request': request})
                texte = serializer.data["intitule"]
                visitor = Visitor.objects.get(token= request.query_params.get("token"))
                visitor.text= texte
                visitor.save()
                print(visitor)
                data = {'texte':texte,'token' :request.query_params.get("token"),'ip' :request.query_params.get("ip_client"),'client_key' : request.query_params.get('client_key')  }
                return render(request, "captcha_audio.html",{'data' : data})
            if request.query_params.get('type') =="image": 
                cap = gen_captcha_img()
                visitor = Visitor.objects.get(token= request.query_params.get("token"))
                visitor.text= cap["cap_text"]
                visitor.save()
                serializer =  VisitorSerializer(visitor,context={'request': request})
                data = {'url' :"http://127.0.0.1:8000/captcha_img/"+cap["name"]+".png",
                'token' :request.query_params.get("token"),'ip' :request.query_params.get("ip_client"),'client_key' :request.query_params.get('client_key')  }
                return render(request,"captcha_image.html",{'data' : data})
        else : 
            return render(request, "")

    def create(self, request, *args, **kwargs):
        print(request.data)
        queryset= Site.objects.all()
        site= get_object_or_404(queryset, public_key= request.data["client_key"])
        print(site)
        if site is not None :
            if request.data["type"]=="image":
                visitor = Visitor.objects.get(token= request.data["token"])
                serializer =  VisitorSerializer(visitor,context={'request': request})
                if(serializer.data["text"] == request.data["text"]):
                    visitor.score = 1.0
                    visitor.save()
            if request.data["type"] =="audio" : 
                visitor = Visitor.objects.get(token= request.data["token"])
                serializer =  VisitorSerializer(visitor,context={'request': request})
                visitor.audio = request.data["audio"]
                r = requests.post(
                'https://speech.googleapis.com/v1p1beta1/speech:recognize',
                    data={
                        "audio": {
                            "content": request.data["audio"]
                        },
                        "config": {
                            "enableAutomaticPunctuation": True,
                            "encoding": "LINEAR16",
                            "languageCode": "fr-FR",
                            "model": "default"
                        }
                        }
                )
                print(r)
                visitor.save()
            return Response({"ip":(serializer.data)['ip'],"token":(serializer.data)['token']}, status=200)
        else : 
            return Response({"error" :"you don't have access"}, status=401)
        
class SignalViewSet(viewsets.ModelViewSet):
    queryset = Signal.objects.all()
    serializer_class = SignalSerializer

class PhrasesViewSet(viewsets.ModelViewSet):
    queryset = Phrases.objects.all()
    serializer_class = PhrasesSerializer

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

@api_view(['POST'])
def getNewPhrase(request):
    queryset = Site.objects.all()
    site= get_object_or_404(queryset, public_key=request.data['client_key'])
    print(site)
    if site is not None :
        anciennePhrase = request.data['anciennePhrase']
        nouvellePhrase = anciennePhrase
        while nouvellePhrase == anciennePhrase :
            code = request.data['codeLangue']
            if code == 'en' : 
                idPhrase = code+str(random.randint(1, 2))
            if code == 'fr' : 
                idPhrase = code+str(random.randint(1, 2))
            print(idPhrase)
            phrase = Phrases.objects.get(id= idPhrase)
            serializer =  PhrasesSerializer(phrase,context={'request': request})
            nouvellePhrase = serializer.data["intitule"]

        return Response({"phrase":nouvellePhrase}, status=200)
    else : 
        return Response({"error" :"you don't have access"}, status=401)




@api_view(['GET'])
def getStart(request):
    queryset = Site.objects.all()
    public_key=request.query_params.get('client_key')
    site= get_object_or_404(queryset,public_key=public_key)
    if site is not None :
        token = ''.join(random.choices(string.ascii_letters +
                 string.digits, k = 20))
        visitor =  Visitor.objects.create(
                    token=token,
                    site = site,
                    score = 0,
                )
        visitor.save()
        serializer =  SiteSerializer(site,context={'request': request})
        signaux = {
            "request" : False,
            "device" : False,
            "behavior" : False,
            "cookie" : False,
        }
        for signal in serializer.data["signals"] :
            signaux[signal] = True
        data = {'token':token,'client_key':public_key,"signaux":signaux}
        return render(request,"box.html",{'data': data})
    else : 
        return Response({"error" :"you don't have access"}, status=401)


@api_view(['POST'])
def getFirstScore(request):
    queryset = Site.objects.all()
    print(request.data)
    site= get_object_or_404(queryset, public_key=request.data['client_key'])
    if site is not None :
        visitor = Visitor.objects.get(token= request.data["token"])
        visitor.ip = request.data["ip_client"]
        visitor.score = random.random()
        visitor.save()
        serializer =  VisitorSerializer(visitor,context={'request': request})
        return Response({"ip":(serializer.data)['ip'],"token":(serializer.data)['token'],"score":True if (float((serializer.data)['score'])>0.5) else False}, status=200)
    else : 
        return Response({"error" :"you don't have access"}, status=401)


@api_view(['POST'])
def getCookie(request):
    queryset = Site.objects.all()
    print(request.data)
    site= get_object_or_404(queryset, public_key=request.data['client_key'])
    if site is not None :
        visitor = Visitor.objects.get(token= request.data["token"])
        visitor.cookie = ''.join(random.choices(string.ascii_letters +
                 string.digits, k = 30))
        visitor.save()
        serializer =  VisitorSerializer(visitor,context={'request': request})
        return Response({"cookie":(serializer.data)['cookie']}, status=200)
    else : 
        return Response({"error" :"you don't have access"}, status=401)

@api_view(['POST'])
def getCookieData(request):
    queryset = Site.objects.all()
    print(request.data)
    site= get_object_or_404(queryset, public_key=request.data['client_key'])
    if site is not None :
        visitor = Visitor.objects.get(cookie= request.data["cookie"])
        visitor.score = random.random()
        visitor.save()
        serializer =  VisitorSerializer(visitor,context={'request': request})
        return Response({"cookie":(serializer.data)['cookie']}, status=200)
    else : 
        return Response({"error" :"you don't have access"}, status=401)
