from django.urls import path , include
from . import views
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from .views import UserViewSet,AuthView

router = DefaultRouter()
router.register(r'users', UserViewSet)

app_name = 'userlist'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
     path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('home/', views.home, name='home'),
    path('api/', include(router.urls)),  # Включение маршрутов API
    path('api/u/email/', views.UserDetailByEmail.as_view(), name='user-detail-by-email'), # получение пользователя по email
    path('api/auth/', AuthView.as_view(), name='auth'),
]