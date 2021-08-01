from django.urls import path

from . import views

urlpatterns = [
    path('server/list/', views.ServerListView.as_view(), name='list_server'),
    path('server/detail/<int:pk>/', views.ServerDetailView.as_view(), name='detail_server')
]
