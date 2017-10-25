from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

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
    
TableDic = {"Player":Player,"TeamLeader":TeamLeader,"TeamMedic":TeamMedic,"TeamCoach":TeamCoach,"Judge":Judge,"Team":Team}
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

    return 0
