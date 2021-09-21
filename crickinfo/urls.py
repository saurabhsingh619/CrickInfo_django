from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^home/', views.index, name='index'),
    url(r'^rankings', views.getRanks, name='getRanks'),
    url(r'^2' , views.team, name='team'),
    url(r'^3' , views.team, name='team'),
    url(r'^4' , views.team, name='team'),
    url(r'^5' , views.team, name='team'),
    url(r'^6' , views.team, name='team'),
    url(r'^9' , views.team, name='team'),
    url(r'^10' , views.team, name='team'),
    url(r'^11' , views.team, name='team'),
    url(r'^12' , views.team, name='team'),
    url(r'^13' , views.team, name='team'),
    url(r'^27' , views.team, name='team'),
    url(r'^96' , views.team, name='team')

]
