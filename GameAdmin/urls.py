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
   
   url(r'^MatchJSON$', views.MatchJSON, name='MatchJSON'),
   url(r'^Set$', views.Set, name='Set'),
]
