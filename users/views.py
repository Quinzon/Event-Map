from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import EventForm
import keys
from map.yandex_api import geocode_address
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from map.models import EventInner
from .forms import ProfileUpdateForm


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


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            location = geocode_address(event.address)
            if location:
                event.location = location
            event.created_by = request.user
            event.save()
            return redirect('home')
    else:
        form = EventForm()
    return render(request, 'users/create_event.html', {'form': form, "Yandex_API": keys.Keys.Yandex_API})


def profile_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404("Пользователь не найден")
    profile = user.profile
    events = EventInner.objects.filter(created_by_id=user)
    return render(request, 'users/profile.html', {'profile': profile, 'events': events})


def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            if not profile.image:
                profile.image = 'default_images/anonymous.svg'
            profile.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile', user_id=request.user.id)
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'users/profile_update.html', {'form': form})
