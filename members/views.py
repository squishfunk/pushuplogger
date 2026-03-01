from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm

def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Rejestracja zakończona sukcesem!")
            return redirect('home')
        else:
            messages.error(request, "Wystąpił błąd podczas rejestracji.")
    else:
        form = RegisterForm()
    return render(request, 'authenticate/register.html', {'form': form})

def login_user(request):
    if request.method=="POST":

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            return redirect('home')

        else:
            messages.success(request, ("Wystąpił błąd podczas logowania"))
            return redirect('login')

    else:
        return render(request, 'authenticate/login.html', {})

def logout_user(request):

    logout(request)
    messages.success(request, ("Wylogowano"))
    return redirect('mainpage')
# Create your views here.
