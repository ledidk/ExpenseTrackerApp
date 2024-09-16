from django.urls import path
from . import views


urlpatterns = [
    path(' ', views.home, name='home'),
    path('index/', views.home, name='home'),
    path('register', views.handleSignupStep1, name='register_step1'),
    path('register/step1/', views.handleSignupStep1, name='register_step1'),
    path('register/step2/', views.handleSignupStep2, name='register_step2'),
    path('register/step3/', views.handleSignupStep3, name='register_step3'),
    path('register/step4/', views.register_success, name='register_step4'),
    path('login/', views.handlelogin, name='handlelogin'),
]