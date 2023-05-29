from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import EventForm
import keys
from map.yandex_api import geocode_address


def register_user(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form})


def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неверный логин или пароль')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('home')


def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            location = geocode_address(event.address)
            if location:
                event.location = location
                event.save()
            else:
                # form.add_error('address', 'Could not geocode this address.')
                return render(request, 'users/create_event.html', {'form': form, "Yandex_API": keys.Keys.Yandex_API})
            return redirect('home')
    else:
        form = EventForm()
    return render(request, 'users/create_event.html', {'form': form, "Yandex_API": keys.Keys.Yandex_API})
