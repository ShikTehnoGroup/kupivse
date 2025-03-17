from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserRegistrationForm , LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate,login
from django.contrib import messages


User = get_user_model()

def home(request):
    return render(request, 'userlist/home.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                print("User authenticated:", user.email)  # Отладочный вывод
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Вы успешно вошли в систему.')
                    return redirect('userlist:home')  # Редирект на домашнюю страницу
                else:
                    messages.error(request, 'Ваша учетная запись отключена.')
            else:
                messages.error(request, 'Неверный логин или пароль.')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = LoginForm()
    return render(request, 'userlist/login.html', {'form': form})



def user_list(request):
    users = User.objects.all()
    return render(request, 'userlist/user_list.html', {'users': users})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'userlist/register_done.html', {'new_user': new_user, 'usermail': new_user.email})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'userlist/register.html', {'user_form': user_form})
