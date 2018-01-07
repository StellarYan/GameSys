# coding=utf-8
from __future__ import unicode_literals
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
    if not IsAdmin(request):
        return HttpResponse('<h1>please login<h1>')
    players = Player.objects.all()
    ScoreList = []
    for p in players:
        for mType in range(1,3):
            pID=p.PlayerID
            pName = Player.objects.filter(PlayerID=pID).values('Name')[0]
            TypeMatchs = Match.objects.filter(MatchType=mType)
            ScoreSum = PlayMatch.objects.filter(PlayerID=pID,MatchID__in=TypeMatchs).aggregate(Sum('AllScore'))
            dic = {'PlayerID':pID,'Name':pName['Name'],'MatchType':mType,'ScoreSum':ScoreSum['AllScore__sum']}
            ScoreList.append(dic)
    jdata = json.dumps(ScoreList)
    return HttpResponse(jdata) #用HttpResponse来返回非django查询生成的json
    
    
#返回的json属性包括团队名称，对应的项目，以及该项目下团队的总成绩。
#查询某一特定项目中，团体单项成绩=ABC赛制，如果这个单项派出的人少于C则为0，否则为分数较高的C个人成绩之和
def GetTeamScore(request):
    if not IsAdmin(request):
        return HttpResponse('<h1>please login<h1>')
    ScoreList=[]
    teams = Team.objects.all()
    for t in teams:
        for mType in range(1,3):
            ScoreList.append(GetTeamScoreByMatchType(t.TeamName,mType))
    jdata = json.dumps(ScoreList)
    return HttpResponse(jdata)  

    
#另外，需要根据赛制求出单个项目中的前X名，作为该项目参与决赛的人员。并自动排出比赛表
#X=4
def GenerateFinal(request):
    if not IsAdmin(request):
        return HttpResponse('<h1>please login<h1>')
    FinalPlayerCount = 4
    NewMatchID = int(Match.objects.aggregate(Max('MatchID'))['MatchID__max'])
    ExistFinalMatch = Match.objects.filter(MatchType=2)
    if ExistFinalMatch.count()>0:
        return HttpResponse("决赛已经被安排")
    for eve in EventTup:
        for grp in GroupTup:
            FirstMatchesWithEveGrp = Match.objects.filter(MatchType=1,Group = grp,Event = eve)
            OrderedPlayers = PlayMatch.objects.filter(MatchID__in=FirstMatchesWithEveGrp).order_by('-AllScore')
            print(FirstMatchesWithEveGrp.count())
            if OrderedPlayers.count()<FinalPlayerCount:
                continue
            NewMatchID+=1
            newMatch = Match()
            newMatch.MatchID = str(NewMatchID)
            newMatch.ChiefID=Judge.objects.get(ID=0)
            newMatch.Group = grp
            newMatch.Event = eve
            newMatch.MatchType=2
            newMatch.save()
            for j in range(0,FinalPlayerCount):
                pm = PlayMatch()
                pm.MatchID = newMatch
                pm.PlayerID =OrderedPlayers[j].PlayerID
                pm.DScore=0
                pm.PScore=0
                pm.AllScore=0
                pm.ScoreState=0
                pm.save();
    return HttpResponse("成功生成决赛")
                
             
            
    

        
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
            #some special process to Match Table
            if(request.POST['Table']=='Match'):
                matchjudge = TableDic['MatchJudge']()
                playmatch = TableDic['PlayMatch']()
                for var in request.POST.getlist('ParticipateJudge'):
                    SetColumn(matchjudge,'ID',var)
                    SetColumn(matchjudge,'MatchID',request.POST['MatchID'])
                    SetColumn(matchjudge,'IsChief',0)
                    matchjudge.save()

                SetColumn(matchjudge,'ID',request.POST['ChiefID_id'])
                SetColumn(matchjudge,'MatchID',request.POST['MatchID'])
                SetColumn(matchjudge,'IsChief',1)
                matchjudge.save()
                for var in request.POST.getlist('ParticipatePlayer'):
                    SetColumn(playmatch,'MatchID',request.POST['MatchID'])
                    SetColumn(playmatch,'PlayerID',var)
                    SetColumn(playmatch,'ScoreState',0)
                    SetColumn(playmatch,'AllScore',0)
                    SetColumn(playmatch,'PScore',0)
                    SetColumn(playmatch,'DScore',0)
                    playmatch.save()
            #end the special process

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
        count = Team.objects.filter(TeamName=name, Password=password).count()
        #管理员登录管理界面
        if name == 'Admin' and password =='123456':
            request.session['isAdmin'] = 'True'
            request.session.set_expiry(3600)
            return render(request, os.path.join("master", "index.html"))
        #代表队登录报名界面（查询数据库内是否存在该帐号且密码是否正确）
        if count > 0:
            team = Team.objects.get(TeamName=name)
            if team.Password == password:
                request.session['TeamName'] = name
                request.session['Password'] = password
                request.session.set_expiry(3600)
                leaderCount = TeamLeader.objects.filter(TeamName=name).count()
                #如果数据库内有该队的记录，则进入EnrollAction页面
                if leaderCount > 0:
                    leader = list(TeamLeader.objects.filter(TeamName=name).values('ID', 'Name', 'PhoneNum'))
                    leaderName = leader[0]['Name']
                    leaderID = leader[0]['ID']
                    leaderTel = leader[0]['PhoneNum']
                    
                    leaderDict = leader[0]

                    medic = list(TeamMedic.objects.filter(TeamName=name).values('ID', 'Name', 'PhoneNum'))
                    medicName = medic[0]['Name']
                    medicID = medic[0]['ID']
                    medicTel = medic[0]['PhoneNum']
                    
                    medicDict = medic[0]

                    playerList = list(Player.objects.filter(TeamName=name).values('PlayerID','ID', 'Name', 'Age', 'Group', 'Event', 'CultureScore'))
                    

                    coachList = list(TeamCoach.objects.filter(TeamName=name).values('ID', 'Name', 'PhoneNum','Gender'))
                    

                    judgeList = list(Judge.objects.filter(TeamName=name).values('ID', 'Name', 'PhoneNum'))
                   

                    return render(request, os.path.join("master", "EnrollAction.html"), {
                        'leaderName': leaderName,
                        'leaderID': leaderID,
                        'leaderTel': leaderTel,
                        'medicName': medicName,
                        'medicID': medicID,
                        'medicTel': medicTel,
                        'LeaderDict': json.dumps(leaderDict),
                        'MedicDict':  json.dumps(medicDict),
                        'PlayerList': json.dumps(playerList),
                        'CoachList':  json.dumps(coachList),
                        'JudgeList':  json.dumps(judgeList)
                    })
                else:
                    return render(request, os.path.join("master", "Enroll.html"))
            else:
                return HttpResponse("<h1>login fail!<h1>")
        #登陆失败
        elif name == None or password == None:
            return HttpResponse("<h1>login fail!<h1>")
    else:
        return render(request, os.path.join("master", "login.html"))
    
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
        cursor = connection.cursor()

        team = Team()
        team.TeamName = request.session.get('TeamName', None)
        team.Password = request.session.get('Password', None)
        team.TeamAccount = team.TeamName
        team.save()

        leader = TeamLeader()
        leader.ID = request.POST["leaderID"]
        leader.Name = request.POST['leaderName']
        leader.PhoneNum = request.POST['leaderTel']
        leader.TeamName_id = request.session.get('TeamName', None)
        leader.save()

        medic = TeamMedic()
        medic.Name = request.POST['DocName']
        medic.ID = request.POST['DocID']
        medic.PhoneNum = request.POST['DocTel']
        medic.TeamName_id = request.session.get('TeamName', None)
        medic.save()

        #多个运动员使用列表/数组
        playerCnt = request.COOKIES['playerCnt']
        playercount = int(playerCnt)
        j = 1
        while j <= playercount:
            player = Player()
            player.Name = request.POST['playerName' + str(j)]
            age = request.POST['playerAge' + str(j)]
            player.Age = int(age)
            player.ID = request.POST['playerID' + str(j)]
            gender = request.POST['sex'+str(j) + 'Option']
            request.session['sex'+str(j)] = gender
            TeamName_id = request.session.get('TeamName', None)
            player.TeamName_id = TeamName_id

            player.CultureScore = 0
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
            id = Player.objects.all().count()
            player.PlayerID = id + 1

            #获取比赛项目列表
            item_list = list(request.POST.getlist('checkbox'+str(j) + 'Option'))
            player.Event = item_list
            print(item_list)
            #根据比赛项目Event和Group获得Match中的MatchID
            request.session['event'+str(j)] = item_list
            '''i = 0
            while item_len > i:
                match = Match()
                Group = player.Group
                Event = item_list[i]
                print("Event:" + Event)
                print("Group:" + Group)
                Match1 = list(Match.objects.all().filter(Event=Event, Group=Group))
                print("MatchID:" + Match1[0].MatchID)
                match.MatchID = Match1[0].MatchID
                i = i + 1'''
            player.save()
            j = j+1

        #多个教练
        coachCnt = request.COOKIES['couchCnt']
        coachcount = int(coachCnt)
        a = 1
        while a <= coachcount:
            coach = TeamCoach()
            coach.ID = request.POST['couchID' + str(a)]
            coach.PhoneNum = request.POST['couchTel' + str(a)]
            coach.Name = request.POST['couchName' + str(a)]
            coach.Gender = request.POST['couchSex' + str(a)]
            coach.TeamName_id = TeamName_id
            coach.save()
            a = a + 1

        #多个裁判
        judgeCnt = request.COOKIES['judgeCnt']
        judgecount = int(judgeCnt)
        z = 1
        while z <= judgecount:
            judge = Judge()
            judge.ID = request.POST['judgeID' + str(z)]
            judge.Name = request.POST['judgeName' + str(z)]
            judge.PhoneNum = request.POST['judgeTel' + str(z)]
            judge.TeamName_id = TeamName_id
            judge.save()
            z = z + 1
        return render(request, os.path.join("master", "EnrollAction.html"))
    else:
        return render(request, os.path.join("master", "login.html"))

#跳转到查看赛事表界面
def EnrollA(request):
    return render(request, os.path.join("master", "Enroll_Playmatch.html"))

#跳转到查看报名表界面（由查看赛事表界面跳转而来）
def EnrollAction(request):
    name = request.COOKIES['TeamName']
    leaderCount = TeamLeader.objects.filter(TeamName=name).count()

    #如果数据库内有该队的记录，则进入EnrollAction页面
    if leaderCount > 0:
        leader = list(TeamLeader.objects.filter(TeamName=name).values('ID', 'Name', 'PhoneNum'))
        leaderName = leader[0]['Name']
        leaderID = leader[0]['ID']
        leaderTel = leader[0]['PhoneNum']
                    
        leaderDict = leader[0]

        medic = list(TeamMedic.objects.filter(TeamName=name).values('ID', 'Name', 'PhoneNum'))
        medicName = medic[0]['Name']
        medicID = medic[0]['ID']
        medicTel = medic[0]['PhoneNum']
                    
        medicDict = medic[0]

        playerList = list(Player.objects.filter(TeamName=name).values('PlayerID','ID', 'Name', 'Age', 'Group', 'Event', 'CultureScore'))
                    

        coachList = list(TeamCoach.objects.filter(TeamName=name).values('ID', 'Name', 'PhoneNum','Gender'))
                    

        judgeList = list(Judge.objects.filter(TeamName=name).values('ID', 'Name', 'PhoneNum'))
                   

        return render(request, os.path.join("master", "EnrollAction.html"), {
            'leaderName': leaderName,
            'leaderID': leaderID,
            'leaderTel': leaderTel,
            'medicName': medicName,
            'medicID': medicID,
            'medicTel': medicTel,
            'LeaderDict': json.dumps(leaderDict),
            'MedicDict':  json.dumps(medicDict),
            'PlayerList': json.dumps(playerList),
            'CoachList':  json.dumps(coachList),
            'JudgeList':  json.dumps(judgeList)
        })
    else:
        return HttpResponse("<h1>发生错误!请重新登录！<h1>")


def ShowScore(request):
    #显示成绩页面
    return render(request,os.path.join("master","Score.html"))
