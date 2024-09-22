from django.urls import path
from . import views

"""
from django.conf.urls import handler404
from home.views import custom_page_not_found_view

handler404 = 'home.views.custom_page_not_found_view'
"""


urlpatterns = [
    path(' ', views.home, name='home'),
    path('index/', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/', views.book_list, name='book_list'),
    path('register', views.handleSignupStep1, name='register_step1'),
    path('register/step1/', views.handleSignupStep1, name='register_step1'),
    path('register/step2/', views.handleSignupStep2, name='register_step2'),
    path('register/step3/', views.handleSignupStep3, name='register_step3'),
    path('register/step4/', views.register_success, name='register_step4'),
    path('signup/', views.handleSignupStep1, name='register_step1'),
    path('login/', views.handlelogin, name='handlelogin'),
    path('reset-password-step1/', views.reset_password_step1, name='reset_password_step1'),
    path('reset-password-step2/', views.reset_password_step2, name='reset_password_step2'),
    path('reset-password-step3/', views.reset_password_step3, name='reset_password_step3'),
]