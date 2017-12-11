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
        return HttpResponse('<h1>please login<h1>')
    return render(request,os.path.join("master","index.html"))
    
def GetPlayer(request):
    if not IsAdmin(request):
        return HttpResponse('<h1>please login<h1>')
    return render(request,os.path.join("master","pages","player.html"))
    
def GetTeamLeader(request):
    if not IsAdmin(request):
        return HttpResponse('<h1>please login<h1>')
    return render(request,os.path.join("master","pages","teamleader.html"))
    
def GetTeamMedic(request):
    if not IsAdmin(request):
        return HttpResponse('<h1>please login<h1>')
    return render(request,os.path.join("master","pages","teammedic.html"))
    
def GetTeamCoach(request):
    if not IsAdmin(request):
        return HttpResponse('<h1>please login<h1>')
    return render(request,os.path.join("master","pages","teamcoach.html"))
    
def GetJudge(request):
    if not IsAdmin(request):
        return HttpResponse('<h1>please login<h1>')
    return render(request,os.path.join("master","pages","judge.html"))
    
def GetTeam(request):
    if not IsAdmin(request):
        return HttpResponse('<h1>please login<h1>')
    return render(request,os.path.join("master","pages","team.html"))
    
def GetMatch(request):
    if not IsAdmin(request):
            return HttpResponse('<h1>please login<h1>')
    return render(request,os.path.join("master","pages","match.html"))
    

def GetJSON(request):
    if not IsAdmin(request):
        return HttpResponse('<h1>please login<h1>')
    if request.method == 'GET':
        tableName =request.GET['Table']
        target_table = TableDic[tableName]
        data = serializers.serialize("json", target_table.objects.all())
        jdata = json.loads(data)
        return JsonResponse(jdata, safe=False)
        
        
def Set(request):
    if not IsAdmin(request):
        return HttpResponse('<h1>please login<h1>')
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
    return render(request,os.path.join("master","login.html"))

def LoginAdmin(request):
    if request.method == 'POST':
        #管理员登录管理界面
        if request.POST['AdminName']=='Admin' and request.POST['password']=='123456':
            request.session['isAdmin'] = 'True'
            request.session.set_expiry(3600)
            return render(request,os.path.join("master","index.html"))
        #代表队登录报名界面
        elif request.POST['AdminName']=='admin' and request.POST['password']=='123456':
            return render(request,os.path.join("master","Enroll.html"))
        #登陆失败
        else:
            return "<h1>login fail</h1>!"

    
def IsAdmin(request):
    if request.session.has_key('isAdmin') and request.session['isAdmin'] == 'True':
        return True
    return False
    
    
def LogoutAdmin(request):
    if request.session.has_key('isAdmin') and request.session['isAdmin'] == 'True':
        request.session['isAdmin'] = 'False'
        return HttpResponse('<h1>logout</h1>')
    else:
        return HttpResponse('not logged in yet')


#处理报名表单信息--插入+查询
def Enroll(request):
    if request.method=="POST":
        team = Team()
        team.File = request.POST['File']
        team.save()

        leader = TeamLeader()
        leader.ID = request.POST["leaderID"]
        leader.Name = request.POST['leaderName']
        leader.PhoneNum = request.POST['leaderTel']
        leader.save()

        medic = TeamMedic()
        medic.Name = request.POST['DocName']
        medic.ID = request.POST['DocID']
        medic.PhoneNum = request.POST['DocTel']
        medic.save()

        player = Player()
        player.Name = request.POST['playerName']
        player.Age = request.POST['playerAge']
        player.ID = request.POST['playerID']
        #生成运动员ID
        ID = Player.objects.filter()
        #获取比赛项目
        event_list = request.POST.getlist['checkbox1Option']

        #if  player.Age >= 7 :
            #根据event和age得到MatchID
        #elif player.Age >=9 :

        #elif player.Age >= 11:

        player.save()

        coach = TeamCoach()
        coach.ID = request.POST['couchID']
        coach.PhoneNum = request.POST['couchTel']
        coach.Name = request.POST['couchName']
        coach.Gender = request.POST['']
        coach.save()

        judge = Judge()
        judge.ID = request.POST['judgeID']
        judge.Name = request.POST['judgeName']
        judge.PhoneNum = request.POST['judgeNameTel']
        judge.save()

        #传给前端数据
        return render(request, 'EnrollAction.html', {'leaderName': leader.Name,'leaderTel':leader.PhoneNum,'leaderID':leader.ID,
                                                     'DocName':medic.Name,'DocTel':medic.PhoneNum,'DocID':medic.ID,
                                                     'playerName':player.Name,'playerAge':player.Age,'playerID':player.Name,
                                                     })


    return render(request,os.path.join("master","EnrollAction.html"))

    

