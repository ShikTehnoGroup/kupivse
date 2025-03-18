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
            if user is not None:
                login(request, user)
                return redirect('userlist:home')
            else:
                form.add_error(None, 'Неверный логин или пароль.')
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
