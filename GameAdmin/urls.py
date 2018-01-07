# coding=utf-8
from django.conf.urls import url

from . import views

urlpatterns = [
   url(r'^$', views.index, name='index'),
   url(r'^Player$', views.GetPlayer, name='GetPlayer'),
   url(r'^TeamLeader$', views.GetTeamLeader, name='GetTeamLeader'),
   url(r'^TeamMedic$', views.GetTeamMedic, name='GetTeamMedic'),
   url(r'^TeamCoach$', views.GetTeamCoach, name='GetTeamCoach'),
   url(r'^Judge$', views.GetJudge, name='GetJudge'),
   url(r'^Team$', views.GetTeam, name='GetTeam'),
   url(r'^GetJSON$', views.GetJSON, name='GetJSON'),
   url(r'^Match$', views.GetMatch, name='GetMatch'),
   url(r'^MatchJudge$', views.GetMatch, name='GetMatch'),
   url(r'^PlayMatch$', views.GetMatch, name='GetMatch'),
   url(r'^Score$', views.GetMatch, name='GetMatch'),
   
   url(r'^AdminLoginTest',views.AdminLoginTest,name='AdminLoginTest'),
   url(r'^LoginAdmin',views.LoginAdmin,name='LoginAdmin'),
   url(r'^LogoutAdmin',views.LogoutAdmin,name='LogoutAdmin'),
   
   #url(r'^MatchJSON$', views.MatchJSON, name='MatchJSON'),
   url(r'^Set$', views.Set, name='Set'),
   url(r'^Enroll$', views.Enroll, name='Enroll'),
   url(r'^EnrollA$', views.EnrollA, name='EnrollA'),
   url(r'^EnrollAction$', views.EnrollAction, name='EnrollAction'),
   url(r'^ShowScore$', views.ShowScore, name='ShowScore'),
   
   url(r'^GetSingleScore$', views.GetSingleScore, name='GetSingleScore'),
   url(r'^GetTeamScore$', views.GetTeamScore, name='GetTeamScore'),
   url(r'^GenerateFinal$',views.GenerateFinal,name='GenerateFinal'),
   
   
   #裁判相关
   url(r'^JudgeLoginTest', views.JudgeLoginTest, name='JudgeLoginTest'),
   url(r'^LoginJudge', views.LoginJudge, name='LoginJudge'),
   url(r'^submitScore', views.submitScore, name='submitScore'),
   #裁判一
   url(r'^Reject$',views.Reject,name='Reject'),
   url(r'^Accept$',views.Accept,name='Accept'),
   #裁判二
   url(r'^Reject2$',views.Reject2,name='Reject2'),
   url(r'^Accept2$',views.Accept2,name='Accept2'),
   #裁判三
   url(r'^Reject3$',views.Reject3,name='Reject3'),
   url(r'^Accept3$',views.Accept3,name='Accept3'),
   #裁判四
   url(r'^Reject4$',views.Reject4,name='Reject4'),
   url(r'^Accept4$',views.Accept4,name='Accept4'),
   #裁判五
   url(r'^Reject5$',views.Reject5,name='Reject5'),
   url(r'^Accept5$',views.Accept5,name='Accept5'),
   url(r'^xsubmitPD',views.xsubmitPD,name='xsubmitPD'),
   url(r'^JudgeIndex$',views.JudgeIndex,name='JudgeIndex'),
   
]
