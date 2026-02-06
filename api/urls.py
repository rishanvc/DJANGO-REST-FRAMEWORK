from django.urls import path

from home.views import index,person,persons_by_team

urlpatterns = [
    path('index/',index,name='index'),
    path('person/',person,name='person'),
    path('team/<int:team_id>/persons/', persons_by_team,name='persons_by_team'),

]
