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


class Score(models.Model):
    class Meta:
        unique_together = (('MatchID','ID', 'PlayerID'),)
    MatchID = models.ForeignKey('Match',on_delete=models.CASCADE,)
    ID = models.ForeignKey('Judge',on_delete=models.CASCADE,)
    PlayerID = models.ForeignKey('Player',on_delete=models.CASCADE,)
    Score = models.IntegerField()
 
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
    
class Player(models.Model):
    PlayerID = models.CharField(max_length=20,primary_key=True)
    ID = models.CharField(max_length=20)
    Name = models.CharField(max_length=20)
    Age = models.IntegerField()
    Group = models.CharField(max_length=20)
    CultureScore = models.IntegerField()
    TeamName = models.ForeignKey('Team',on_delete=models.CASCADE,)
    
    
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
    
    
class Team(models.Model):
    TeamName = models.CharField(max_length=20,primary_key=True)
    TeamAccount = models.CharField(max_length=20)
    Password = models.CharField(max_length=20)
    File =models.FileField(upload_to='uploads/', max_length=100)
    
TableDic = {"Player":Player,"TeamLeader":TeamLeader,"TeamMedic":TeamMedic,
"TeamCoach":TeamCoach,"Judge":Judge,"Team":Team,
"PlayMatch":PlayMatch,"Score":Score,"MatchJudge":MatchJudge,"Match":Match}
    
def GetTargetTable(request):
    tableName = request.POST['Table']
    return TableDic[tableName]
    
    
def GetTargetObj(request,target_table):
    if(target_table!=PlayMatch and target_table!=Score and target_table!=MatchJudge):
        if(request.POST['Type']=='Upgrade'):
            print(target_table._meta.pk.name)
            print(request.POST['ID'])
            print(request.POST[target_table._meta.pk.name]) 
            return target_table.objects.get(pk=request.POST[target_table._meta.pk.name])
        if(request.POST['Type']=='Delete'):
            return target_table.objects.get(pk=request.POST['pk'])
            
            
          
def SetColumn(tobj,fieldName,fieldValue):
    target_table =TableDic[type(tobj).__name__]
    if(hasattr(target_table, fieldName)):
        if(isinstance(getattr(target_table, fieldName),ForwardManyToOneDescriptor)):
            setattr(tobj,fieldName+"_id",fieldValue)#对于外键，django 会自动在对象的field的后面加上_id，这里补上即可
        else:
            setattr(tobj,fieldName,fieldValue)
    
    




