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
from django.template import loader ,Context

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
            newMatch.MatchStatus='Waiting'
            newMatch.save()
            #添加裁判
            tmp = 0
            for judge in TableDic['Judge'].objects.all():
                #print(judge.ID)
                newJudge=MatchJudge()
                newJudge.MatchID = newMatch
                newJudge.ID = judge
                if tmp == 5:
                    newJudge.IsChief = 'True'
                    newJudge.save()
                    break
                newJudge.IsChief = 'False'
                newJudge.save()
                tmp = tmp + 1
                pass
            for j in range(0,FinalPlayerCount):
                pm = PlayMatch()
                pm.MatchID = newMatch
                pm.PlayerID =OrderedPlayers[j].PlayerID
                pm.DScore=0
                pm.PScore=0
                pm.AllScore=0
                pm.ScoreState=0
                pm.save()
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
                for var in request.POST.getlist('ParticipateJudge'):
                    matchjudge = TableDic['MatchJudge']()
                    print(var)
                    SetColumn(matchjudge,'ID',var)
                    SetColumn(matchjudge,'MatchID',request.POST['MatchID'])
                    SetColumn(matchjudge,'IsChief',0)
                    print(matchjudge.ID_id)
                    matchjudge.save()
                matchjudge = TableDic['MatchJudge']()
                SetColumn(matchjudge,'ID',request.POST['ChiefID_id'])
                SetColumn(matchjudge,'MatchID',request.POST['MatchID'])
                SetColumn(matchjudge,'IsChief',1)
                matchjudge.save()
                for var in request.POST.getlist('ParticipatePlayer'):
                    playmatch = TableDic['PlayMatch']()
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
        else:
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
            TeamName_id = request.session.get('TeamName', None)
            coach.TeamName_id = TeamName_id
            coach.save()
            a = a + 1

        #多个裁判
        judgeCnt = request.COOKIES['judgeCnt']
        judgecount = int(judgeCnt)
        print(judgecount)
        z = 1
        while z <= judgecount:
            judge = Judge()
            judge.ID = request.POST['judgeID' + str(z)]
            judge.Name = request.POST['judgeName' + str(z)]
            judge.PhoneNum = request.POST['judgeTel' + str(z)]
            TeamName_id = request.session.get('TeamName', None)
            judge.TeamName_id = TeamName_id
            judge.save()
            z = z + 1

        #显示报名信息界面
        leader = list(TeamLeader.objects.filter(TeamName=TeamName_id).values('ID', 'Name', 'PhoneNum'))
        leaderName = leader[0]['Name']
        leaderID = leader[0]['ID']
        leaderTel = leader[0]['PhoneNum']
                    
        leaderDict = leader[0]

        medic = list(TeamMedic.objects.filter(TeamName=TeamName_id).values('ID', 'Name', 'PhoneNum'))
        medicName = medic[0]['Name']
        medicID = medic[0]['ID']
        medicTel = medic[0]['PhoneNum']
                    
        medicDict = medic[0]

        playerList = list(Player.objects.filter(TeamName=TeamName_id).values('PlayerID','ID', 'Name', 'Age', 'Group', 'Event', 'CultureScore'))
                    

        coachList = list(TeamCoach.objects.filter(TeamName=TeamName_id).values('ID', 'Name', 'PhoneNum','Gender'))
                    

        judgeList = list(Judge.objects.filter(TeamName=TeamName_id).values('ID', 'Name', 'PhoneNum'))
                   

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
        return render(request, os.path.join("master", "EnrollAction.html"))
    else:
        return render(request, os.path.join("master", "login.html"))

def EnrollA(request):
    return render(request, os.path.join("master", "Enroll_Playmatch.html"))
def EnrollAction(request):
    Name = request.session.get("TeamName","")
    TeamName_id = str(Name)
    leaderCount = TeamLeader.objects.filter(TeamName=TeamName_id).count()
    #如果数据库内有该队的记录，则进入EnrollAction页面
    if leaderCount > 0:
        #显示报名信息界面
        leader = list(TeamLeader.objects.filter(TeamName=TeamName_id).values('ID', 'Name', 'PhoneNum'))
        leaderName = leader[0]['Name']
        leaderID = leader[0]['ID']
        leaderTel = leader[0]['PhoneNum']
                    
        leaderDict = leader[0]

        medic = list(TeamMedic.objects.filter(TeamName=TeamName_id).values('ID', 'Name', 'PhoneNum'))
        medicName = medic[0]['Name']
        medicID = medic[0]['ID']
        medicTel = medic[0]['PhoneNum']
                    
        medicDict = medic[0]

        playerList = list(Player.objects.filter(TeamName=TeamName_id).values('PlayerID','ID', 'Name', 'Age', 'Group', 'Event', 'CultureScore'))
                    

        coachList = list(TeamCoach.objects.filter(TeamName=TeamName_id).values('ID', 'Name', 'PhoneNum','Gender'))
                    

        judgeList = list(Judge.objects.filter(TeamName=TeamName_id).values('ID', 'Name', 'PhoneNum'))
                   

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
        return render(request, os.path.join("master", "login.html"))

    

def ShowScore(request):
    #显示成绩页面
    return render(request,os.path.join("master","Score.html"))








#裁判相关
def JudgeLoginTest(request):
    return render(request, os.path.join("master", "Login2.html"))

def LoginJudge(request):
    if request.method == 'POST':
        judge = Judge.objects.filter(JudgeAccount=request.POST['JudgeName'], Password=request.POST['password'])
            #print("******")
        #judge = Judge.objects.filter(JudgeAccount=request.POST['JudgeName'], Password=request.POST['password'])
        if len(judge) == 1:
            return IndexJudge(request, judge)
        else:
            return HttpResponse('用户名或密码输入错误')
    else:
        judge=Judge.objects.filter(ID=request.session['JudgeID'])
        print(request.session['JudgeID'])
        print(judge)
        return IndexJudge(request, judge)

def IndexJudge(request,judge):
    #if request.method == 'POST':
        request.session['JudgeID']=judge[0].ID
        judge=Judge.objects.filter(ID=request.session['JudgeID'])
        #request.session['judge'] = judge
        #if not any(judge):
         #   judge=request.session['judge']
        c = 0
        a = Match.objects.filter(MatchStatus="Running")
        for i in a:
            b = MatchJudge.objects.filter(MatchID_id=i.MatchID)
            for j in b:
                if j.ID_id == judge[0].ID:
                    c = 1
        if c == 0:
            return HttpResponse('当前没有您的比赛');
        else:
            if len(Match.objects.filter(ChiefID_id=judge[0].ID)) == 0:
                a = json.dumps(2)
                pobjects1 = PlayMatch.objects.filter(ScoreState=1)
                if (len(pobjects1)==0):
                    return HttpResponse('您的评分以通过')
                else:
                    pobjects=pobjects1[0]
                PlayerID = pobjects.PlayerID_id
                PlayerName = Player.objects.get(PlayerID=PlayerID).Name
                MatchID = pobjects.MatchID_id
                JudgeID = judge[0].ID
                score = Score.objects.get(MatchID_id=MatchID, PlayerID_id=PlayerID, ID_id=judge[0].ID).Score
                Event = Match.objects.get(MatchID=MatchID).Event
                ScoreAccept = Score.objects.get(MatchID_id=MatchID, PlayerID_id=PlayerID, ID_id=judge[0].ID).ScoreAccept
                list = {'Event': Event, 'PlayerName': PlayerName, 'MatchID': MatchID,
                        'PlayerID': PlayerID, 'Score': int(score),
                        'ScoreAccept': ScoreAccept}
                request.session['ID_id'] = judge[0].ID
                request.session['MatchID_id'] = MatchID
                request.session['PlayerID'] = PlayerID
                request.session['Event'] = Event
                request.session['PlayerName'] = PlayerName
                request.session['a'] = a

            else:
                # list = {"Event": "单杠", "PlayerName": "张三", "MatchID": 00, "PlayerID": 00, "ScoreState": "Running",
                #           "Score1": 3, "ScoreAccept1": 0, "Score2": 4, "ScoreAccept2": 1, "Score3": 5,
                #          "ScoreAccept3": 2, "Score4": "-1", "ScoreAccept4": 0, "Score5": "-1", "ScoreAccept5": 0, }
                a = json.dumps(1)
                pobjects = PlayMatch.objects.filter(ScoreState=1)
                if (len(pobjects) == 0):
                    return HttpResponse('正在准备下一位运动员的比赛')
                pobjects = pobjects[0]
                MatchID = pobjects.MatchID_id
                Event = Match.objects.get(MatchID=MatchID).Event
                PlayerID = pobjects.PlayerID_id
                PlayerName = Player.objects.get(PlayerID=PlayerID).Name
                Scorelist = Score.objects.filter(MatchID_id=MatchID, PlayerID_id=PlayerID).order_by(
                    'ID_id').values_list('Score')
                JudgeIDlist = MatchJudge.objects.filter(MatchID_id=MatchID, IsChief=0).order_by('ID_id').values_list(
                    'ID_id')
                ScoreAcceptlist = Score.objects.filter(MatchID_id=MatchID, PlayerID_id=PlayerID).order_by(
                    'ID_id').values_list('ScoreAccept')
                request.session['mainID_id'] = judge[0].ID
                request.session['mainMatchID_id'] = MatchID
                request.session['mainPlayerID'] = PlayerID
                request.session['mainEvent'] = Event
                request.session['mainPlayerName'] = PlayerName
                request.session['maina'] = a
                request.session['a']=a
                list = {'Event': Event, 'PlayerName': PlayerName, 'MatchID': MatchID,
                        'PlayerID': PlayerID, 'ScoreState': "Running",
                        'Score1': Scorelist[0], 'ScoreAccept1': ScoreAcceptlist[0], 'JudgeID1': JudgeIDlist[0],
                        'Score2': Scorelist[1], 'ScoreAccept2': ScoreAcceptlist[1], 'JudgeID2': JudgeIDlist[1],
                        'Score3': Scorelist[2], 'ScoreAccept3': ScoreAcceptlist[2], 'JudgeID3': JudgeIDlist[2],
                        'Score4': Scorelist[3], 'ScoreAccept4': ScoreAcceptlist[3], 'JudgeID4': JudgeIDlist[3],
                        'Score5': Scorelist[4], 'ScoreAccept5': ScoreAcceptlist[4], 'JudgeID5': JudgeIDlist[4]}
                request.session['mainlist'] = list
            return render(request, "master/pages/Index2.html", {'flag': a, 'list': json.dumps(list)})

def submitScore(request):
    if request.method == 'POST':
        score1 = request.POST['SScore']
        PlayerID=request.session['PlayerID']
        ID_id=request.session['ID_id']
        Event=request.session['Event']
        MatchID_id=request.session['MatchID_id']
        PlayerName=request.session['PlayerName']
        a=request.session['a']
        obj=Score.objects.get(PlayerID=PlayerID,MatchID=MatchID_id,ID_id=ID_id)
        obj.Score=int(score1)
        obj.ScoreAccept=0
        obj.save()
        list = {'Event': Event, 'PlayerName': PlayerName, 'MatchID': MatchID_id, 'PlayerID': PlayerID, 'Score': score1,
                'ScoreAccept': 0}
        print(score1)
        print("**************")
        #把分数写入数据库
        # 这里查询一下flag和list的信息，然后把两个值传回Index2.html
        # return render(request, os.path.join("master", "Index2.html"), {'list': json.dumps(list), 'flag': 2})
        return render(request, "master/pages/Index2.html", {'flag': a, 'list': json.dumps(list)})
    else:
        return  HttpResponseRedirect('http://127.0.0.1:8000/GameAdmin/LoginJudge')


# 主裁判提交P分D分
def xsubmitPD(request):
    print("submitPD")
    if request.method == 'POST':
        PScore = request.POST['PScore']
        DScore = request.POST['DScore']
        #value1 = request.COOKIES["PScore"]
        #value2 = request.COOKIES["DScore"]
        MatchID=request.session['mainMatchID_id']
        PlayerID=request.session['mainPlayerID']
        Event=request.session['mainEvent']
        PlayerName=request.session['PlayerName']
        list=request.session['mainlist']
        a=request.session['a']
        obj=PlayMatch.objects.get(PlayerID_id=PlayerID,MatchID_id=MatchID)
        obj.DScore=int(DScore)
        obj.PScore=int(PScore)
        obj.ScoreState=2
        obj.save()
        a=0
        # 写数据
        return render(request, "master/pages/Index2.html", {'flag': a, 'list': json.dumps(list)})



def Reject(request):
    #拒绝裁判一的分数，想数据库执行写操作
    #拿到flag和list，返回Index2.html
    MatchID = request.COOKIES["MatchID"]
    PlayerID = request.COOKIES["PlayerID"]
    JudgeID = request.COOKIES["JudgeID1"]
    Score1 = request.COOKIES["Score1"]
    ScoreAccept = request.COOKIES["ScoreAccept1"]
    obj = Score.objects.get(PlayerID=PlayerID, MatchID=MatchID,ID_id=JudgeID)
    obj.Score = int(Score1)
    obj.ScoreAccept=1
    obj.save()
    list = request.session['mainlist']
    ScoreAcceptlist = Score.objects.filter(MatchID_id=MatchID, PlayerID_id=PlayerID).order_by('ID_id').values_list(
        'ScoreAccept')
    list['ScoreAccept1']=ScoreAcceptlist[0]
    list['ScoreAccept2'] = ScoreAcceptlist[1]
    list['ScoreAccept3'] = ScoreAcceptlist[2]
    list['ScoreAccept4'] = ScoreAcceptlist[3]
    list['ScoreAccept5'] = ScoreAcceptlist[4]
    return render(request, "master/pages/Index2.html", {'flag': 1, 'list': json.dumps(list)})


def Accept(request):
    print("拒绝1")
    #接受裁判一的分数，执行写操作
    # 拿到flag和list，返回Index2.html
    MatchID = request.COOKIES["MatchID"]
    PlayerID = request.COOKIES["PlayerID"]
    JudgeID = request.COOKIES["JudgeID1"]
    Score1 = request.COOKIES["Score1"]
    ScoreAccept = request.COOKIES["ScoreAccept1"]
    obj = Score.objects.get(PlayerID=PlayerID, MatchID=MatchID,ID_id=JudgeID)
    obj.Score = int(Score1)
    obj.ScoreAccept=2
    obj.save()
    list = request.session['mainlist']
    ScoreAcceptlist = Score.objects.filter(MatchID_id=MatchID, PlayerID_id=PlayerID).order_by('ID_id').values_list(
        'ScoreAccept')
    list['ScoreAccept1']=ScoreAcceptlist[0]
    list['ScoreAccept2'] = ScoreAcceptlist[1]
    list['ScoreAccept3'] = ScoreAcceptlist[2]
    list['ScoreAccept4'] = ScoreAcceptlist[3]
    list['ScoreAccept5'] = ScoreAcceptlist[4]
    return render(request, "master/pages/Index2.html", {'flag': 1, 'list': json.dumps(list)})



#裁判二
def Reject2(request):
    #拒绝裁判二的分数，想数据库执行写操作
    #拿到flag和list，返回Index2.html
    MatchID = request.COOKIES["MatchID"]
    PlayerID = request.COOKIES["PlayerID"]
    JudgeID = request.COOKIES["JudgeID2"]
    Score1 = request.COOKIES["Score2"]
    ScoreAccept = request.COOKIES["ScoreAccept2"]
    obj = Score.objects.get(PlayerID=PlayerID, MatchID=MatchID,ID_id=JudgeID)
    obj.Score = int(Score1)
    obj.ScoreAccept=1
    obj.save()
    list = request.session['mainlist']
    ScoreAcceptlist = Score.objects.filter(MatchID_id=MatchID, PlayerID_id=PlayerID).order_by('ID_id').values_list(
        'ScoreAccept')
    list['ScoreAccept1']=ScoreAcceptlist[0]
    list['ScoreAccept2'] = ScoreAcceptlist[1]
    list['ScoreAccept3'] = ScoreAcceptlist[2]
    list['ScoreAccept4'] = ScoreAcceptlist[3]
    list['ScoreAccept5'] = ScoreAcceptlist[4]
    return render(request, "master/pages/Index2.html", {'flag': 1, 'list': json.dumps(list)})

def Accept2(request):
    print("拒绝2")
    #接受裁判二的分数，执行写操作
    # 拿到flag和list，返回Index2.html
    MatchID = request.COOKIES["MatchID"]
    PlayerID = request.COOKIES["PlayerID"]
    JudgeID = request.COOKIES["JudgeID2"]
    Score1 = request.COOKIES["Score2"]
    ScoreAccept = request.COOKIES["ScoreAccept2"]
    obj = Score.objects.get(PlayerID=PlayerID, MatchID=MatchID,ID_id=JudgeID)
    obj.Score = int(Score1)
    obj.ScoreAccept=2
    obj.save()
    list = request.session['mainlist']
    ScoreAcceptlist = Score.objects.filter(MatchID_id=MatchID, PlayerID_id=PlayerID).order_by('ID_id').values_list(
        'ScoreAccept')
    list['ScoreAccept1']=ScoreAcceptlist[0]
    list['ScoreAccept2'] = ScoreAcceptlist[1]
    list['ScoreAccept3'] = ScoreAcceptlist[2]
    list['ScoreAccept4'] = ScoreAcceptlist[3]
    list['ScoreAccept5'] = ScoreAcceptlist[4]
    return render(request, "master/pages/Index2.html", {'flag': 1, 'list': json.dumps(list)})



#裁判三
def Reject3(request):
    #拒绝裁判二的分数，想数据库执行写操作
    #拿到flag和list，返回Index2.html
    MatchID = request.COOKIES["MatchID"]
    PlayerID = request.COOKIES["PlayerID"]
    JudgeID = request.COOKIES["JudgeID3"]
    Score1 = request.COOKIES["Score3"]
    ScoreAccept = request.COOKIES["ScoreAccept3"]
    obj = Score.objects.get(PlayerID=PlayerID, MatchID=MatchID,ID_id=JudgeID)
    obj.Score = int(Score1)
    obj.ScoreAccept=1
    obj.save()
    list = request.session['mainlist']
    ScoreAcceptlist = Score.objects.filter(MatchID_id=MatchID, PlayerID_id=PlayerID).order_by('ID_id').values_list(
        'ScoreAccept')
    list['ScoreAccept1']=ScoreAcceptlist[0]
    list['ScoreAccept2'] = ScoreAcceptlist[1]
    list['ScoreAccept3'] = ScoreAcceptlist[2]
    list['ScoreAccept4'] = ScoreAcceptlist[3]
    list['ScoreAccept5'] = ScoreAcceptlist[4]
    return render(request, "master/pages/Index2.html", {'flag': 1, 'list': json.dumps(list)})


def Accept3(request):
    print("拒绝3")
    #接受裁判二的分数，执行写操作
    # 拿到flag和list，返回Index2.html
    MatchID = request.COOKIES["MatchID"]
    PlayerID = request.COOKIES["PlayerID"]
    JudgeID = request.COOKIES["JudgeID3"]
    Score1 = request.COOKIES["Score3"]
    ScoreAccept = request.COOKIES["ScoreAccept3"]
    obj = Score.objects.get(PlayerID=PlayerID, MatchID=MatchID,ID_id=JudgeID)
    obj.Score = int(Score1)
    obj.ScoreAccept=2
    obj.save()
    list = request.session['mainlist']
    ScoreAcceptlist = Score.objects.filter(MatchID_id=MatchID, PlayerID_id=PlayerID).order_by('ID_id').values_list(
        'ScoreAccept')
    list['ScoreAccept1']=ScoreAcceptlist[0]
    list['ScoreAccept2'] = ScoreAcceptlist[1]
    list['ScoreAccept3'] = ScoreAcceptlist[2]
    list['ScoreAccept4'] = ScoreAcceptlist[3]
    list['ScoreAccept5'] = ScoreAcceptlist[4]
    return render(request, "master/pages/Index2.html", {'flag': 1, 'list': json.dumps(list)})



#裁判四
def Reject4(request):
    #拒绝裁判二的分数，想数据库执行写操作
    #拿到flag和list，返回Index2.html
    MatchID = request.COOKIES["MatchID"]
    PlayerID = request.COOKIES["PlayerID"]
    JudgeID = request.COOKIES["JudgeID4"]
    Score1 = request.COOKIES["Score4"]
    ScoreAccept = request.COOKIES["ScoreAccept4"]
    obj = Score.objects.get(PlayerID=PlayerID, MatchID=MatchID,ID_id=JudgeID)
    obj.Score = int(Score1)
    obj.ScoreAccept=1
    obj.save()
    list = request.session['mainlist']
    ScoreAcceptlist = Score.objects.filter(MatchID_id=MatchID, PlayerID_id=PlayerID).order_by('ID_id').values_list(
        'ScoreAccept')
    list['ScoreAccept1']=ScoreAcceptlist[0]
    list['ScoreAccept2'] = ScoreAcceptlist[1]
    list['ScoreAccept3'] = ScoreAcceptlist[2]
    list['ScoreAccept4'] = ScoreAcceptlist[3]
    list['ScoreAccept5'] = ScoreAcceptlist[4]
    return render(request, "master/pages/Index2.html", {'flag': 1, 'list': json.dumps(list)})

def Accept4(request):
    print("拒绝4")
    #接受裁判二的分数，执行写操作
    # 拿到flag和list，返回Index2.html
    MatchID = request.COOKIES["MatchID"]
    PlayerID = request.COOKIES["PlayerID"]
    JudgeID = request.COOKIES["JudgeID4"]
    Score1 = request.COOKIES["Score4"]
    ScoreAccept = request.COOKIES["ScoreAccept4"]
    obj = Score.objects.get(PlayerID=PlayerID, MatchID=MatchID,ID_id=JudgeID)
    obj.Score = int(Score1)
    obj.ScoreAccept=2
    obj.save()
    list = request.session['mainlist']
    ScoreAcceptlist = Score.objects.filter(MatchID_id=MatchID, PlayerID_id=PlayerID).order_by('ID_id').values_list(
        'ScoreAccept')
    list['ScoreAccept1']=ScoreAcceptlist[0]
    list['ScoreAccept2'] = ScoreAcceptlist[1]
    list['ScoreAccept3'] = ScoreAcceptlist[2]
    list['ScoreAccept4'] = ScoreAcceptlist[3]
    list['ScoreAccept5'] = ScoreAcceptlist[4]
    return render(request, "master/pages/Index2.html", {'flag': 1, 'list': json.dumps(list)})



#裁判五
def Reject5(request):
    #拒绝裁判二的分数，想数据库执行写操作
    #拿到flag和list，返回Index2.html
    MatchID = request.COOKIES["MatchID"]
    PlayerID = request.COOKIES["PlayerID"]
    JudgeID = request.COOKIES["JudgeID5"]
    Score1 = request.COOKIES["Score5"]
    ScoreAccept = request.COOKIES["ScoreAccept5"]
    obj = Score.objects.get(PlayerID=PlayerID, MatchID=MatchID,ID_id=JudgeID)
    obj.Score = int(Score1  )
    obj.ScoreAccept=1
    obj.save()
    list = request.session['mainlist']
    ScoreAcceptlist = Score.objects.filter(MatchID_id=MatchID, PlayerID_id=PlayerID).order_by('ID_id').values_list(
        'ScoreAccept')
    list['ScoreAccept1']=ScoreAcceptlist[0]
    list['ScoreAccept2'] = ScoreAcceptlist[1]
    list['ScoreAccept3'] = ScoreAcceptlist[2]
    list['ScoreAccept4'] = ScoreAcceptlist[3]
    list['ScoreAccept5'] = ScoreAcceptlist[4]
    return render(request, "master/pages/Index2.html", {'flag': 1, 'list': json.dumps(list)})


def Accept5(request):
    #接受裁判二的分数，执行写操作
    # 拿到flag和list，返回Index2.html
    MatchID = request.COOKIES["MatchID"]
    PlayerID = request.COOKIES["PlayerID"]
    JudgeID = request.COOKIES["JudgeID5"]
    Score1 = request.COOKIES["Score5"]
    ScoreAccept = request.COOKIES["ScoreAccept5"]
    obj = Score.objects.get(PlayerID=PlayerID, MatchID=MatchID,ID_id=JudgeID)
    obj.Score = int(Score1)
    obj.ScoreAccept=2
    obj.save()
    list = request.session['mainlist']
    ScoreAcceptlist = Score.objects.filter(MatchID_id=MatchID, PlayerID_id=PlayerID).order_by('ID_id').values_list(
        'ScoreAccept')
    list['ScoreAccept1']=ScoreAcceptlist[0]
    list['ScoreAccept2'] = ScoreAcceptlist[1]
    list['ScoreAccept3'] = ScoreAcceptlist[2]
    list['ScoreAccept4'] = ScoreAcceptlist[3]
    list['ScoreAccept5'] = ScoreAcceptlist[4]
    return render(request, "master/pages/Index2.html", {'flag': 1, 'list': json.dumps(list)})


def JudgeIndex(request):
    if request.method == 'GET':
        list=request.session['mainlist']
        ID=request.session['ID_id']
        judge=Judge.objects.get(ID=ID)
        try:
            c = 0
            a = Match.objects.filter(MatchStatus="Running")
            for i in a:
                b = MatchJudge.objects.filter(MatchID_id=i.MatchID)
                for j in b:
                    if j.ID_id == judge.ID:
                        c = 1
            if (c==0):
                return HttpResponse("当前没有您的比赛")
            else:
                if len(Match.objects.filter(CheifID_id=ID))==1:
                    a=1
                else :
                    a=2
        except:
            pass
        finally:
            pass
        list['a']=a
        data = serializers.serialize("json", list)
        """"
        tableName = request.GET['Table']
        target_table = TableDic[tableName]
        queryset = target_table.objects.all()
        try:
            matchid = request.GET['MatchID']
            queryset = target_table.objects.filter(MatchID__exact=matchid)
        except:
            pass
        finally:
            pass

        data = serializers.serialize("json", queryset)
        """
        jdata = json.loads(data)
        return JsonResponse(jdata, safe=False)
