from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserRegistrationForm , LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate,login,authenticate
from django.contrib import messages


User = get_user_model()

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

def new_user_login(request, user):
    # Используем кастомный бэкенд для аутентификации
    email = user.email
    password = user.password  # Убедитесь, что вы используете правильный способ получения пароля

    # Аутентификация через кастомный бэкенд
    authenticated_user = authenticate(request, email=email, password=password)
    
    if authenticated_user is not None:
        login(request, authenticated_user)  # Вход в систему
    else:
        print("Аутентификация не удалась")


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
            
            new_user_login(request, new_user)
            # Возвращаем JSON-ответ
            return JsonResponse({'success': True, 'message': 'Регистрация успешна!', 'redirect_url': '/userlist/home'})
        else:
            # Возвращаем ошибки валидации в JSON-формате
            return JsonResponse({'success': False, 'errors': user_form.errors}, status=400)
    else:
        user_form = UserRegistrationForm()
    return render(request, 'userlist/register.html', {'user_form': user_form})