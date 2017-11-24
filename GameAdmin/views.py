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
    if not IsAdmin(request):
        return HttpResponse('please login')
    return render(request,os.path.join("master","index.html"))
    
def GetPlayer(request):
    if not IsAdmin(request):
        return HttpResponse('please login')
    return render(request,os.path.join("master","pages","player.html"))
    
def GetTeamLeader(request):
    if not IsAdmin(request):
        return HttpResponse('please login')
    return render(request,os.path.join("master","pages","teamleader.html"))
    
def GetTeamMedic(request):
    if not IsAdmin(request):
        return HttpResponse('please login')
    return render(request,os.path.join("master","pages","teammedic.html"))
    
def GetTeamCoach(request):
    if not IsAdmin(request):
        return HttpResponse('please login')
    return render(request,os.path.join("master","pages","teamcoach.html"))
    
def GetJudge(request):
    if not IsAdmin(request):
        return HttpResponse('please login')
    return render(request,os.path.join("master","pages","judge.html"))
    
def GetTeam(request):
    if not IsAdmin(request):
        return HttpResponse('please login')
    return render(request,os.path.join("master","pages","team.html"))
    
def GetMatch(request):
    if not IsAdmin(request):
            return HttpResponse('please login')
    return render(request,os.path.join("master","pages","match.html"))
    

def GetJSON(request):
    if not IsAdmin(request):
        return HttpResponse('please login')
    if request.method == 'GET':
        tableName =request.GET['Table']
        target_table = TableDic[tableName]
        data = serializers.serialize("json", target_table.objects.all())
        jdata = json.loads(data)
        return JsonResponse(jdata, safe=False)
        
        
def Set(request):
    if not IsAdmin(request):
        return HttpResponse('please login')
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
        
        
def AdminLoginTest(request):
    return render(request,os.path.join("master","AdminLoginTest.html"))

def LoginAdmin(request):
    if request.method == 'POST':
        if request.POST['AdminName']=='Admin' and request.POST['password']=='123456':
            request.session['isAdmin'] = 'True'
            request.session.set_expiry(3600)
        else:
            return "login fail!"
    return index(request)

    
def IsAdmin(request):
    if request.session.has_key('isAdmin') and request.session['isAdmin'] == 'True':
        return True
    return False
    
    
def LogoutAdmin(request):
    if request.session.has_key('isAdmin') and request.session['isAdmin'] == 'True':
        request.session['isAdmin'] = 'False'
        return HttpResponse('logout')
    else:
        return HttpResponse('not logged in yet')
    
    
    

    
    

