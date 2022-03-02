"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import *

urlpatterns = [

    path('aviators/list/', AviatorListView.as_view()),
    path('users/create/<int:aviator_id>/', UserCreateView.as_view()),
    path('users/detail/<int:pk>/', UserDetailView.as_view()),
    path('aviators/fromuser/<int:user_id>/', AviatorFromUserListView.as_view()),
    path('prospective_aviators/detail/', ProspectiveAviatorDetailView.as_view()),
    path('stats/', StatsView.as_view()),
    path('stats/flightlog/list/<aviator_pk>/', FlightLogListView.as_view()),
    path('stats/flightlog/aggregate/<int:aviator_pk>/', FlightLogAggregateView.as_view()),
    path('stats/flightlog/timeseries/<int:aviator_pk>/<int:time_span>/', FlightLogTimeSeriesView.as_view()),
    path('stats/combatlog/list/<int:aviator_pk>/', CombatLogListView.as_view()),
    path('stats/combatlog/aggregate/<int:aviator_pk>/', CombatLogAggregateView.as_view()),
    path('stats/combatlog/timeseries/<int:aviator_pk>/<int:time_span>/', CombatLogTimeSeriesView.as_view()),
    path('squadrons/list/', SquadronListView.as_view()),
    path('hqs/list/', HQListView.as_view()),
    path('modules/list/', DCSModuleListView.as_view()),
    path('event/list/', EventListView.as_view()),
    path('event/list/<str:start>/<str:end>/', EventListView.as_view()),
    path('event/detail/<int:pk>/', EventDetailView.as_view()),
    path('documentation/list/', DocumentationListView.as_view()),
    path('documentation/modules/list/', DocumentationModuleListView.as_view()),
    path('user_images/list/', UserImageListView.as_view()),
    path('munition/list/', MunitionListView.as_view()),
    path('stores/', StoresView.as_view()),
    path('target/list/', TargetListView.as_view()),
    path('stores/list/<str:name>/', StoresListView.as_view()),
    path('operation/list/', OperationListView.as_view()),
    path('liveries/update/', AviatorLiveriesListView.as_view()),
    path('rq/queue/status/', RqQueueStatusListView.as_view())

]
