from django.urls import path
from . import views

app_name = 'userlist'
urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('home/', views.home, name='home'),
    
]