from django.db import models

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
        unique_together = (('MatchID','JudgeID', 'PlayerID'),)
    MatchID = models.ForeignKey('Match',on_delete=models.CASCADE,)
    JudgeID = models.ForeignKey('Judge',on_delete=models.CASCADE,)
    PlayerID = models.ForeignKey('Player',on_delete=models.CASCADE,)
    Score = models.IntegerField()
 
class MatchJudge(models.Model):
    class Meta:
        unique_together = (('MatchID','JudgeID'),)
    MatchID = models.ForeignKey('Match',on_delete=models.CASCADE,)
    JudgeID = models.ForeignKey('Judge',on_delete=models.CASCADE,)
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
    age = models.IntegerField()
    Group = models.CharField(max_length=20)
    CultrueScore = models.IntegerField()
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
    Name = models.CharField(max_length=20,primary_key=True)
    TeamAccount = models.CharField(max_length=20)
    Password = models.CharField(max_length=20)
    File =models.FileField(upload_to='uploads/', max_length=100)



