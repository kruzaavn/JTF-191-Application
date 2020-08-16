from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path('server/list/', views.ServerListView.as_view(), name='list_server'),
    path('server/detail/<int:pk>/', views.ServerDetailView.as_view(), name='detail_server')
]
