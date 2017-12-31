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
        name = request.POST['AdminName']
        password = request.POST['password']
        #管理员登录管理界面
        if name == 'Admin' and password =='123456':
            request.session['isAdmin'] = 'True'
            request.session.set_expiry(3600)
            return render(request,os.path.join("master","index.html"))
        elif name == 'admin1' and password =='123456':
            return render(request,os.path.join("master","Enroll.html"))
        #代表队登录报名界面（查询数据库内是否存在该帐号且密码是否正确）
        elif Team.objects.filter(TeamName = name) and Team.objects.filter(Team):
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
    if request.method == "POST":
        #team = Team()
        #team.File = request.POST['File']
        #team.save()

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

        #多个运动员使用列表/数组
        playerCount = request.POST['']
        j = 1
        while j <= playeraccount:
            player= Player()
            player.Name = request.POST['playerName' + str(j)]
            player.Age = request.POST['playerAge' + str(j)]
            player.ID = request.POST['playerID' + str(j)]
            gender = request.POST.get['sex1Option' + str(j)]
            #根据年龄性别分组
            if 7 <= player.Age <= 8:
                if gender == 'option1':
                    player.Group = 'Male1'
                else:
                    player.Group = 'Female1'
            elif 9 <= player.Age <= 10:
                if gender == 'option1':
                    player.Group = 'Male2'
                else:
                    player.Group = 'Female2'
            else:
                if gender == 'option1':
                    player.Group = 'Male3'
                else:
                    player.Group = 'Female3'
            #生成运动员player.playerID
            id = Player.objects.values("playerID").filter(max('playerID'))
            player.playerID = id + 1
            #获取比赛项目列表
            item_list = request.POST.getlist['checkbox1Option']
            #根据比赛项目Event和Group获得Match中的MatchID
            item_len = len(item_list)
            match = Match()
            match.Group = player.Group
            i = 0
            while item_len > i:
                match.Event = item_list[i]
                matchID = Match.objects.values('MatchID').filter('Event' == match.Event and 'Group' == match.Group)
                match.MatchID = matchID
                match.save()
                i = i + 1
            player.save()
            j = j+1

        #多个教练
        coachCount = request.POST['']
        i = 1
        while i <= coachCount:
            coach = TeamCoach()
            coach.ID = request.POST['couchID' + str(i)]
            coach.PhoneNum = request.POST['couchTel' + str(i)]
            coach.Name = request.POST['couchName' + str(i)]
            coach.Gender = request.POST['couchSex' + str(i)]
            coach.save()

        #多个裁判
        judgeCount = request.POST['']
        i = 1
        while i <= judgeCount:
            judge = Judge()
            judge.ID = request.POST['judgeID' + str(i)]
            judge.Name = request.POST['judgeName' + str(i)]
            judge.PhoneNum = request.POST['judgeNameTel' + str(i)]
            judge.save()

        #测试
    return HttpResponse('报名成功！')

def EnorllAction(request):
    return 

#return render(request, 'EnrollAction.html', {'leaderName': leader.Name, 'leaderTel': leader.PhoneNum, 'leaderID': leader.ID,
#                                                     'DocName': medic.Name, 'DocTel': medic.PhoneNum, 'DocID': medic.ID,
#                                                     'playerName': player.Name, 'playerAge': player.Age , 'playerID': player.Name,
#})

    #else:
        #return render(request,os.path.join("master","EnrollAction.html"))


def EnrollA(request):
        #获取运动员数目的cookie
        value1 = request.COOKIES["playerCnt"]
        value2 = request.COOKIES["judgeCnt"]
        value3 = request.COOKIES["couchCnt"]
        #返回收到的cookies值
        #return HttpResponse(str(value1) )
        return render(request,os.path.join("master","Enroll.html"))

