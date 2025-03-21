from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'userlist'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
     path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('home/', views.home, name='home'),
    
]