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


# (PlayMatch)报名参赛表: [比赛号 运动员号] D分 P分

# (Score)比赛打分表: [比赛号 裁判身份证 运动员号] 成绩 

# (MatchJudge)比赛裁判表：[比赛号 裁判身份证] 是否是主裁判

# (Match)比赛表: [比赛号] 比赛年龄组 项目 主裁判身份证 预期开始时间 预期结束时间

# (Player)运动员表: [运动员号] 身份证 姓名 年龄 比赛年龄组 文化成绩 参与的比赛项目 小队名称 

# (TeamLeader)领队信息表: [身份证] 姓名 电话 小队名称

# (TeamMedic)队医信息表:  [身份证] 姓名 电话 小队名称

# (TeamCoach)教练员信息表: [身份证] 姓名 电话 性别 小队名称

# (Judge)裁判员信息表: [身份证] 裁判账号(uni) 姓名  电话 密码

# (Team)小队表: [小队名称] 账号(uni) 密码  {每个代表队还需要以文件的方式提交附件}

# (GameAdmin)管理员账号表：[账号] 密码
