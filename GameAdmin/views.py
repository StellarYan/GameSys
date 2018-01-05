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

def GetSingleScore(request):
    pass
#返回的json属性包含姓名,运动员ID和个人参加的所有项目的成绩总和
#PlayMatch 表根据运动员号查总分
#Player 表根据运动员号查姓名
def GetTeamScore(request):
    pass
#返回的json属性包括团队名称，对应的项目，以及该项目下团队的总成绩。
#查询某一特定项目中，团体单项成绩=ABC赛制，如果这个单项派出的人少于C则为0，否则为分数较高的C个人成绩之和

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
            item_list = request.POST.getlist('checkbox'+str(j) + 'Option')
            #根据比赛项目Event和Group获得Match中的MatchID
            item_len = len(item_list)
            print(item_list)
            request.session['event'+str(j)] = item_list

            i = 0
            while item_len > i:
                match = Match()
                Group = player.Group
                Event = item_list[i]
                print("Event:" + Event)
                print("Group:" + Group)
                Match1 = list(Match.objects.all().filter(Event=Event, Group=Group))
                print("MatchID:" + Match1[0].MatchID)
                match.MatchID = Match1[0].MatchID
                i = i + 1
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
            z = z + 1
            judge.save()
        return render(request, os.path.join("master", "EnrollAction.html"))
    else:
        return render(request, os.path.join("master", "Enroll.html"))

def EnrollA(request):
    if request.method == 'POST':
        response = render(request, os.path.join("master","EnrollAction.html"))

        TeamName = request.session.get('TeamName', None)

        leader = TeamLeader.objects.filter(TeamName=TeamName)
        leaderName = leader.Name
        leaderID =leader.ID
        leaderPhone = leader.PhoneNum
        response.set_cookie('leaderName', leaderName)
        response.set_cookie('leaderID', leaderID)
        response.set_cookie('leaderPhone', leaderPhone)

        medic = TeamMedic.objects.filter(TeamName=TeamName)
        medicName = medic.Name
        medicID = medic.ID
        medicPhone = medic.PhoneNum
        response.set_cookie('medicName', medicName)
        response.set_cookie('medicID', medicID)
        response.set_cookie('medicPhone', medicPhone)

        couchCnt = request.COOKIES["couchCnt"]
        coachcount = int(couchCnt)
        coach = TeamCoach.objects.filter(TeamName=TeamName)
        if coachcount > 0:
            i = 0
            for c in coach:
                coachName = c.Name
                coachID = c.ID
                coachPhone = c.PhoneNum
                coachSex = c.Gender
                response.set_cookie('coachName'+str(i), coachName)
                response.set_cookie('coachID'+str(i), coachID)
                response.set_cookie('coachPhone'+str(i), coachPhone)
                response.set_cookie('coachSex'+str(i), coachSex)
                i = i + 1

        judgeCnt = request.COOKIES["judgeCnt"]
        judgecount = int(judgeCnt)
        judge = Judge.objects.filter(TeamName=TeamName)
        if judgecount > 0:
            j = 0
            for a in judge:
                judgeName = a.Name
                judgeID = a.ID
                judgePhone = a.PhoneNum
                response.set_cookie('judgeName'+str(j), judgeName)
                response.set_cookie('judgeID'+str(j), judgeID)
                response.set_cookie('judgePhone'+str(j), judgePhone)
                j = j + 1

        playerCnt = request.COOKIES["judgeCnt"]
        playercount = int(playerCnt)
        player = Player.objects.filter(TeamName_id=TeamName)
        if playercount > 0:
            z = 0
            for p in player:
                playerName = p.Name
                playerID = p.ID
                playerAge = p.Age
                playerGroup = p.Group
                playerEvent = request.session.get('event'+str(z))
                playerSex = request.session.get('sex'+str(z))
                response.set_cookie('playerName'+str(z), playerName)
                response.set_cookie('playerID'+str(z), playerID)
                response.set_cookie('playerAge'+str(z), playerAge)
                response.set_cookie('playerGroup'+str(z), playerGroup)
                response.set_cookie('playerEvent'+str(z), playerEvent)
                z = z + 1

    return render(request, os.path.join("master", "EnrollAction.html"))


def ShowScore(request):
    #显示成绩页面
    return render(request,os.path.join("master","Score.html"))
