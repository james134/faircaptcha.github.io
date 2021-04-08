from django.db import models

# Create your models here.

class Signal(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    description = models.CharField(max_length=100, null=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class Site(models.Model):
    url = models.CharField(max_length=100, null=False)
    email =  models.CharField(max_length=100, null = False)
    public_key = models.CharField(max_length=100, null=False)
    secret_key = models.CharField(max_length=100, null=False)
    signals = models.ManyToManyField(Signal)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.public_key


class Visitor(models.Model):
    token = models.CharField(max_length=100, null=True)
    ip = models.CharField(max_length=100, null=False)
    score = models.FloatField(null=True)
    text = models.CharField(max_length=100, null=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.ip
