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

from django.db import connection
from itertools import chain
from django.db.models import Sum
from django.db.models import Count
from django.db.models import Max


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
        queryset = target_table.objects.all()
        try: 
            matchid = request.GET['MatchID']
            queryset = target_table.objects.filter(MatchID__exact=matchid)
        except:
            pass
        finally:
            pass
        
        data = serializers.serialize("json",queryset )
        jdata = json.loads(data)
        return JsonResponse(jdata, safe=False)

#返回的json属性包含姓名,运动员ID和个人参加的所有项目的成绩总和
#PlayMatch 表根据运动员号查总分
#Player 表根据运动员号查姓名
def GetSingleScore(request):
    pID=request.GET['PlayerID']
    pName = Player.objects.filter(PlayerID=pID).values('Name')[0]
    ScoreSum = PlayMatch.objects.filter(PlayerID=pID).aggregate(Sum('AllScore'))
    dic = {'PlayerID':pID,'Name':pName['Name'],'ScoreSum':ScoreSum['AllScore__sum']}
    jdata = json.dumps(dic)
    return HttpResponse(jdata) #用HttpResponse来返回非django查询生成的json
    
    
#返回的json属性包括团队名称，对应的项目，以及该项目下团队的总成绩。
#查询某一特定项目中，团体单项成绩=ABC赛制，如果这个单项派出的人少于C则为0，否则为分数较高的C个人成绩之和
def GetTeamScore(request):
    tName = request.GET['TeamName']
    Rule_PlayerCountInGroupScore = GlobeMatchRule.objects.all().values('PlayerCountInGroupScore')[0]['PlayerCountInGroupScore']
    TeamPlayers = Player.objects.filter(TeamName=tName)
    EventScore = {}
    for eve in EventTup:
        EventMatchs = Match.objects.filter(Event=eve)
        queryPlayMatch = PlayMatch.objects.filter(PlayerID__in=TeamPlayers,MatchID__in=EventMatchs)
        EventPlayercount = queryPlayMatch.count()
        if EventPlayercount<Rule_PlayerCountInGroupScore:
            EventScore[eve] = 0
        else:
            EventPlayerScores = queryPlayMatch.order_by('-AllScore').values('AllScore')
            EventScore[eve]=0
            for j in range(0,Rule_PlayerCountInGroupScore):
                EventScore[eve] += EventPlayerScores[j]['AllScore']
    jdata = json.dumps(EventScore)
    return HttpResponse(jdata)  

    
#另外，需要根据赛制求出单个项目中的前X名，作为该项目参与决赛的人员。并自动排出比赛表

        
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

def ShowScore(request):
    #显示成绩页面
    return render(request,os.path.join("master","Score.html"))