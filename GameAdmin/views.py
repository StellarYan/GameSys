from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields import Field
from django.db.models import ForeignKey
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor


import json
import os.path



from .models import PlayMatch
from .models import Score
from .models import MatchJudge
from .models import Match
from .models import Player
from .models import TeamLeader
from .models import TeamMedic
from .models import TeamCoach
from .models import Judge
from .models import Team

TableDic = {"Player":Player,"TeamLeader":TeamLeader,"TeamMedic":TeamMedic,
"TeamCoach":TeamCoach,"Judge":Judge,"Team":Team,
"PlayMatch":PlayMatch,"Score":Score,"MatchJudge":MatchJudge,"Match":Match}

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

    # print("-------------")
    # f = Judge._meta.get_fields()[3]
    # t = Judge.objects.all()[0]
    # if(isinstance(f, Field)):
        # print(f.name)
        # print(hasattr(t, "ID"))
        
    # print("-------------")
    
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
        tableName =request.POST['Table']
        target_table = TableDic[tableName]
        if(target_table!=PlayMatch and target_table!=Score and target_table!=MatchJudge and target_table!=Match):
            if(request.POST['Type']=='Upgrade'):
                tobj=target_table.objects.get(pk=request.GET['pk'])
                for para in request.POST:
                    if(hasattr(tobj, para)):
                        setattr(tobj,para,request.POST[para])
            elif(request.POST['Type']=='Add'):
                newobj = target_table()
                print(hasattr(target_table, "TeamName"))
                for para in request.POST:
                    print("----")
                    if(hasattr(target_table, para)):
                        print(type(getattr(target_table, para)))
                        if(isinstance(getattr(target_table, para),ForwardManyToOneDescriptor)):
                            setattr(newobj,para+"_id",request.POST[para])#对于外键，django会自动在对象的field的后面加上_id，这里补上即可
                        else:
                            setattr(newobj,para,request.POST[para])
                newobj.save()
            elif(request.POST['Type']=='Delete'):
                tobj=target_table.objects.get(pk=request.POST['pk'])
                print('Delte')
                print(tobj)
                tobj.delete()
        
    return render(request,os.path.join("master","pages","match.html"))
