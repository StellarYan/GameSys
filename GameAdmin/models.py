from django.db import models
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
# Create your models here.



class PlayMatch(models.Model):
    class Meta:
        unique_together = (('MatchID', 'PlayerID'),)
    MatchID = models.ForeignKey('Match',on_delete=models.CASCADE,)
    PlayerID = models.ForeignKey('Player',on_delete=models.CASCADE,)
    DScore = models.IntegerField()
    PScore = models.IntegerField()
    AllScore = models.IntegerField()
    ScoreState = models.IntegerField()


class Score(models.Model):
    class Meta:
        unique_together = (('MatchID','ID', 'PlayerID'),)
    MatchID = models.ForeignKey('Match',on_delete=models.CASCADE,)
    ID = models.ForeignKey('Judge',on_delete=models.CASCADE,)
    PlayerID = models.ForeignKey('Player',on_delete=models.CASCADE,)
    Score = models.IntegerField()
    ScoreAccept = models.IntegerField(default=0)
 
class MatchJudge(models.Model):
    class Meta:
        unique_together = (('MatchID','ID'),)
    MatchID = models.ForeignKey('Match',on_delete=models.CASCADE,)
    ID = models.ForeignKey('Judge',on_delete=models.CASCADE,)
    IsChief = models.BooleanField(default=0)

class Match(models.Model):
    MatchID = models.CharField(max_length=20,primary_key=True)
    Group = models.CharField(max_length=20)
    Event = models.CharField(max_length=20)
    ChiefID = models.ForeignKey('Judge',on_delete=models.CASCADE,)
    StartTime = models.CharField(max_length=20)
    EndTime = models.CharField(max_length=20)
    MatchStatus = models.CharField(max_length=20)
    MatchType = models.CharField(max_length=10)
    SubGroup = models.CharField(max_length=10)
    
class Player(models.Model):
    PlayerID = models.CharField(max_length=20,primary_key=True)
    ID = models.CharField(max_length=20)
    Name = models.CharField(max_length=20)
    Age = models.IntegerField()
    Group = models.CharField(max_length=20)
    CultureScore = models.IntegerField()
    TeamName = models.ForeignKey('Team',on_delete=models.CASCADE,)
    Event = models.CharField(max_length=60)
    
    
class TeamLeader(models.Model):
    ID = models.CharField(max_length=20,primary_key=True)
    Name = models.CharField(max_length=20)
    PhoneNum = models.CharField(max_length=20)
    TeamName = models.ForeignKey('Team',on_delete=models.CASCADE,)
    
class TeamMedic(models.Model):
    ID = models.CharField(max_length=20,primary_key=True)
    Name = models.CharField(max_length=20)
    PhoneNum = models.CharField(max_length=20)
    TeamName = models.ForeignKey('Team',on_delete=models.CASCADE,)
    
class TeamCoach(models.Model):
    ID = models.CharField(max_length=20,primary_key=True)
    Name = models.CharField(max_length=20)
    PhoneNum = models.CharField(max_length=20)
    Gender = models.CharField(max_length=1)
    TeamName = models.ForeignKey('Team',on_delete=models.CASCADE,)

class Judge(models.Model):
    ID = models.CharField(max_length=20,primary_key=True)
    JudgeAccount = models.CharField(max_length=20)
    Password = models.CharField(max_length=20)
    Name = models.CharField(max_length=20)
    PhoneNum = models.CharField(max_length=20)
    TeamName = models.ForeignKey('Team',on_delete=models.CASCADE,)
    
    
class Team(models.Model):
    TeamName = models.CharField(max_length=20, primary_key=True)
    TeamAccount = models.CharField(max_length=20)
    Password = models.CharField(max_length=20)
    File = models.FileField(upload_to='uploads/', max_length=100)
    
class GlobeMatchRule(models.Model):
    TeamPlayerPerGroup = models.IntegerField()
    PlayerPerMatch = models.IntegerField()
    PlayerCountInGroupScore = models.IntegerField()
    
    
TableDic = {"Player": Player, "TeamLeader": TeamLeader, "TeamMedic": TeamMedic,
"TeamCoach": TeamCoach, "Judge": Judge, "Team": Team,
"PlayMatch": PlayMatch, "Score": Score, "MatchJudge": MatchJudge, "Match":Match,
"GlobeMatchRule":GlobeMatchRule}

EventTup = ('DG','SG','DH','TN','TC','AM','BC','GD','PH')
#单杠 双杠 吊环 跳马 体操 鞍马 蹦床 高低杠 平衡木 

GroupTup = ('Female1','Female2','Female3','Male1','Male2','Male3')



def GetTargetTable(request):
    tableName = request.POST['Table']
    return TableDic[tableName]
    
    
def GetTargetObj(request,target_table):
    if(target_table!=PlayMatch and target_table!=Score and target_table!=MatchJudge):
        if(request.POST['Type']=='Upgrade'):
            return target_table.objects.get(pk=request.POST[target_table._meta.pk.name])
        if(request.POST['Type']=='Delete'):
            return target_table.objects.get(pk=request.POST['pk'])
    else:
        #objs = target_table.objects.all()
        my_filter = {}
        for tid in target_table._meta.unique_together[0]:
            print("LLLLLLL")
            print(tid)
            print(request.POST[tid])
            my_filter[tid] = request.POST[tid]
        objs=target_table.objects.filter(**my_filter)
        return objs.first()
        
            
            
          
def SetColumn(tobj,fieldName,fieldValue):
    target_table =TableDic[type(tobj).__name__]
    if fieldName=='id':
        return
    if(hasattr(target_table, fieldName)):
        if(isinstance(getattr(target_table, fieldName),ForwardManyToOneDescriptor)):
            setattr(tobj,fieldName+"_id",fieldValue)
        else:
            setattr(tobj,fieldName,fieldValue)
            
            
def GetTeamScoreByMatchType(teamName,matchType):
    EvegrpScoreList = []
    Rule_PlayerCountInGroupScore = GlobeMatchRule.objects.all().values('PlayerCountInGroupScore')[0]['PlayerCountInGroupScore']
    TeamPlayers = Player.objects.filter(TeamName=teamName)
    for eve in EventTup:
        for grp in GroupTup:
            TeamScoreList={}
            TeamScoreList['TeamName']=teamName
            TeamScoreList['Event']=eve
            TeamScoreList['Group']=grp
            TeamScoreList['MatchType']=matchType
            EventMatchs = Match.objects.filter(Event=eve).filter(Group=grp).filter(MatchType=matchType)
            queryPlayMatch = PlayMatch.objects.filter(PlayerID__in=TeamPlayers,MatchID__in=EventMatchs)
            EventPlayercount = queryPlayMatch.count()
            if EventPlayercount<Rule_PlayerCountInGroupScore:
                TeamScoreList['GroupScore'] = 0
            else:
                EventPlayerScores = queryPlayMatch.order_by('-AllScore').values('AllScore')
                TeamScoreList['GroupScore']=0
                for j in range(0,Rule_PlayerCountInGroupScore):
                    TeamScoreList['GroupScore']+=EventPlayerScores[j]['AllScore']
            EvegrpScoreList.append(TeamScoreList)
    return EvegrpScoreList
            
            

    
    
    




