from django.http import HttpResponse
from django.shortcuts import render
from j3dpscalc.models import GlobalParam

# Create your views here.

def index(request):
    try:
        s = GlobalParam.objects.all()
        return HttpResponse(s)
    except:
        return HttpResponse("没有找到对应的信息！")