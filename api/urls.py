from django.urls import path,include

from home.views import index,person,persons_by_team,ClassPerson,PersonViewSets,RegisterAPI,LoginAPI
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'mdvs', PersonViewSets, basename='mdvs')


urlpatterns = [
    path('',include(router.urls)),
    path('index/',index,name='index'),
    path('person/',person,name='person'),
    path('team/<int:team_id>/persons/', persons_by_team,name='persons_by_team'),
    path('classperson/',ClassPerson.as_view(),name='classperson'),

    
    # AUTH URLs (ADD THESE)
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),

]
