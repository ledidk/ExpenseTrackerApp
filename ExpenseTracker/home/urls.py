from django.urls import path
from . import views


urlpatterns = [
    path(' ', views.home, name='home'),
    path('index/', views.home, name='home'),
    path('register', views.handleSignup, name='handleSignup'),
    path('login/', views.handlelogin, name='handlelogin'),
]