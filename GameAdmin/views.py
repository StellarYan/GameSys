# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields import Field
from django.db.models import ForeignKey
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
from django.http import HttpResponseRedirect  
from django.core.urlresolvers import reverse
from django.http import HttpResponse


import json
import os.path




from .models import *



def index(request):
    return render(request,os.path.join("master","index.html"))
    
def GetPlayer(request):
    return render(request,os.path.join("master","pages","player.html"))
    
def GetTeamLeader(request):
    return render(request,os.path.join("master","pages","teamleader.html"))
    
def GetTeamMedic(request):
    return render(request,os.path.join("master","pages","teammedic.html"))
    
def GetTeamCoach(request):
    return render(request,os.path.join("master","pages","teamcoach.html"))
    
def GetJudge(request):
    return render(request,os.path.join("master","pages","judge.html"))
    
def GetTeam(request):
    return render(request,os.path.join("master","pages","team.html"))
    

def GetJSON(request):
    if request.method == 'GET':
        tableName =request.GET['Table']
        target_table = TableDic[tableName]
        data = serializers.serialize("json", target_table.objects.all())
        jdata = json.loads(data)
        return JsonResponse(jdata, safe=False)


    
def GetMatch(request):
    return render(request,os.path.join("master","pages","match.html"))
    
def MatchJSON(request):
    return 0
    
def Set(request):
    print('-------Start Set--------')
    if request.method == 'POST':
        target_table = GetTargetTable(request)
        if(request.POST['Type']=='Upgrade'):
            tobj=GetTargetObj(request,target_table)
            for para in request.POST:
                SetColumn(tobj,para,request.POST[para])
            tobj.save()
        elif(request.POST['Type']=='Add'):
            newobj = target_table()
            for para in request.POST:
                SetColumn(newobj,para,request.POST[para])
            newobj.save()
        elif(request.POST['Type']=='Delete'):
            tobj=GetTargetObj(request,target_table)
            tobj.delete()
        return HttpResponse('OK')
