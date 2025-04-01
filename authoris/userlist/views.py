from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserRegistrationForm , LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate,login
from django.contrib import messages
from rest_framework import viewsets,generics, status
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import Users
from rest_framework.views import APIView

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

class UserDetailByEmail(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        print("UserDetailByEmail.get called")  # Логируем вызов метода
        email = request.query_params.get('email', None)  # Получаем email из параметров запроса
        print(f"Received email: {email}")  # Логируем полученный email
        if email is not None:
            try:
                user = Users.objects.get(email=email)  # Ищем пользователя по email
                serializer = self.get_serializer(user)
                return Response(serializer.data)  # Возвращаем данные пользователя
            except Users.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "Email parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

class AuthView(APIView): # апи аутентификация 
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            return Response({"message": "Authentication successful", "user": {"email": user.email}}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


def index(request):
    return render(request, 'userlist/index.html')

def home(request):
    return render(request, 'userlist/home.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('userlist:home')
            else:
                if user is None:
                    form.add_error(None, 'Неверный логин или пароль.')
                elif not user.is_active:
                    form.add_error(None, 'Ваш аккаунт неактивен.')
                    print(form.non_field_errors)
    else:
        form = LoginForm()
    return render(request, 'userlist/login.html', {'form': form})




def user_list(request):
    users = User.objects.all()
    return render(request, 'userlist/user_list.html', {'users': users})

from django.http import JsonResponse
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаем новый объект пользователя, но не сохраняем его сразу
            new_user = user_form.save(commit=False)
            # Устанавливаем выбранный пароль
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохраняем объект пользователя
            new_user.save()
            
            login(request, new_user)
            # Возвращаем JSON-ответ
            return JsonResponse({'success': True, 'message': 'Регистрация успешна!', 'redirect_url': '/userlist/home'})
        else:
            # Возвращаем ошибки валидации в JSON-формате
            return JsonResponse({'success': False, 'errors': user_form.errors}, status=400)
    else:
        user_form = UserRegistrationForm()
    return render(request, 'userlist/register.html', {'user_form': user_form})