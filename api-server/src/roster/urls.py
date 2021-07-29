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
    path('aviators/detail/<int:pk>/', AviatorDetailView.as_view()),
    path('prospective_aviators/detail/', ProspectiveAviatorDetailView.as_view()),
    path('stats/', StatsView.as_view()),
    path('squadrons/list/', SquadronListView.as_view()),
    path('hqs/list/', HQListView.as_view()),
    path('modules/list/', DCSModuleListView.as_view()),
    path('event/list/', EventListView.as_view()),
    path('event/detail/<int:pk>/', EventDetailView.as_view()),
    path('qualifications/list/', QualificationListView.as_view()),
    path('qualifications/detail/<int:pk>', QualificationDetailView.as_view()),
    path('qualifications/modules/list/', QualificationModuleListView.as_view()),
    path('qualifications/modules/detail/<int:pk>', QualificationModuleDetailView.as_view()),
    path('qualifications/checkoffs/list/', QualificationCheckoffListView.as_view()),
    path('qualifications/checkoffs/detail/<int:pk>', QualificationCheckoffDetailView.as_view()),
    path('munition/list/', MunitionListView.as_view()),
    path('stores/list/', StoresListView.as_view()),
    #path('operation/list/',OperationListView.as_view())

]
