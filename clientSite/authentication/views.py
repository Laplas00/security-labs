from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login

def dashboard(request):
    return render(request, 'auth/welcome.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST['username'].lower()
        email    = request.POST['email']
        password = request.POST['password1']
        confirm  = request.POST['password2']

        if password != confirm:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'aauth/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Имя пользователя уже занято')
            return render(request, 'auth/register.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        auth_login(request, user)

        return redirect('dashboard')

    return render(request, 'auth/register.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            print('error')
            messages.error(request, 'Неверное имя пользователя или пароль')
            return render(request, 'auth/login.html')

    return render(request, 'auth/login.html')


