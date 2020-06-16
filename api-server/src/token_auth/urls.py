from django.urls import path
from rest_framework_simplejwt import views

# Create your views here.

urlpatterns = [

    path('token/', views.TokenObtainPairView.as_view()),
    path('refresh/', views.TokenRefreshView.as_view())

]