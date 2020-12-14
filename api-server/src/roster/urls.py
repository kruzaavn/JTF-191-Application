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

    path('aviator', AviatorListView.as_view()),
    path('user/create/<int:aviator_id>', UserCreateView.as_view()),
    path('user/<int:pk>', UserDetailView.as_view()),
    path('aviators/<int:pk>', AviatorDetailView.as_view()),
    path('prospective_aviator', ProspectiveAviatorDetailView.as_view()),
    path('stats', StatsView.as_view()),
    path('squadron', SquadronListView.as_view()),
    path('hq', HQListView.as_view()),
    path('module', DCSModuleListView.as_view()),
    path('event', EventListView.as_view()),
    path('event/<int:pk>', EventDetailView.as_view()),
    path('qualification', QualificationListView.as_view()),
    path('qualification/<int:pk>', QualificationDetailView.as_view()),
    path('qualifications/module', QualificationModuleListView.as_view()),
    path('qualifications/modules/<int:pk>', QualificationModuleDetailView.as_view()),
    path('qualifications/checkoff', QualificationCheckoffListView.as_view()),
    path('qualifications/checkoff/<int:pk>', QualificationCheckoffDetailView.as_view()),

]
