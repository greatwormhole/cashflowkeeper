from django.contrib.auth.models import User 
from django.contrib.auth.forms import (
    AuthenticationForm, 
    UserCreationForm,
    PasswordResetForm
    )
from django.contrib.auth import authenticate, login, logout 
from django.shortcuts import render, redirect
from django.contrib import messages

def loginPage(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is invalid')

    content = {'form': form}
    return render(request, 'accounts/login_form.html', content)

def logoutPage(request):
    logout(request)
    return redirect('/')

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Произошла ошибка при регистрации')
    content = {'form': form}
    return render(request, 'accounts/register_form.html', content)

def passrecPage(request):
    form = PasswordResetForm()
    content = {'form': form}
    return render(request, 'accounts/passrec.html', content)