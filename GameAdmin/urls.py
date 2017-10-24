from django.conf.urls import url

from . import views

urlpatterns = [
   url(r'^$', views.index, name='index'),
   url(r'^Player$', views.Player, name='Player'),
   url(r'^TeamLeader$', views.TeamLeader, name='TeamLeader'),
   url(r'^TeamMedic$', views.TeamMedic, name='TeamMedic'),
   url(r'^TeamCoach$', views.TeamCoach, name='TeamCoach'),
   url(r'^Judge$', views.Judge, name='Judge'),
   url(r'^Team$', views.Team, name='Team'),
   url(r'^GetJSON$', views.GetJSON, name='GetJSON'),
   url(r'^Match$', views.Match, name='Match'),
   url(r'^MatchJSON$', views.MatchJSON, name='MatchJSON'),
   url(r'^Set$', views.Set, name='Set'),
]
