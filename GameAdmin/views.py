from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


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

    return 0
    
def Player(request):
    return render(request,r"master/pages/player.html")
    
def TeamLeader(request):
    return render(request,r"master/pages/teamleader.html")
    
def TeamMedic(request):
    return render(request,r"master/pages/teammedic.html")
    
def TeamCoach(request):
    return render(request,r"master/pages/teamcoach.html")
    
def Judge(request):
    return render(request,r"master/pages/judge.html")
    
def Team(request):
    return render(request,r"master/pages/team.html")
    
def GetJSON(request):
    if request.method == 'GET':
        data = serializers.serialize("json", Match.objects.all())
        jdata = json.loads(data)
        return JsonResponse(jdata, safe=False)
    
def Match(request):
    return render(request,r"master/pages/match.html")
    
def MatchJSON(request):

    return 0
    
def Set(request):

    return 0
