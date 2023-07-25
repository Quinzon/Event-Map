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
from map.models import EventInner, EventAPI
from .forms import ProfileUpdateForm
from django.views.decorators.csrf import csrf_exempt
from users.models import Profile, UserFavoriteProfile, UserFavoriteEvent
from django.http import JsonResponse
from itertools import chain


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
    favorite_profiles = UserFavoriteProfile.objects.filter(user_id=user)
    if request.user.is_authenticated:
        subscribe_to_profiles_ids = UserFavoriteProfile.objects.filter(user=request.user).values_list('profile_id',
                                                                                                      flat=True)
        subscribe_to_events_ids = UserFavoriteEvent.objects.filter(user=request.user).values_list('event_inner_id',
                                                                                                  flat=True)
    else:
        subscribe_to_profiles_ids = False
        subscribe_to_events_ids = False
    return render(request, 'users/profile.html', {'profile': profile,
                                                  'events': events,
                                                  'favorite_profiles': favorite_profiles,
                                                  'subscribe_to_profiles_ids': subscribe_to_profiles_ids,
                                                  'subscribe_to_events_ids': subscribe_to_events_ids})


def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            if not profile.image:
                profile.image = 'default_images/anonymous.svg'
            if not profile.background_image:
                profile.background_image = 'default_images/profile_background_image.svg'
            profile.save()
            return redirect('profile', user_id=request.user.id)
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'users/profile_update.html', {'form': form})


@csrf_exempt
def toggle_profile_subscription(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        profile_id = request.POST.get('profile_id')

        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(id=profile_id)

        subscription, created = UserFavoriteProfile.objects.get_or_create(user=user, profile=profile)

        if not created:
            subscription.delete()
            return JsonResponse({'subscribed': False})

        return JsonResponse({'subscribed': True})


@login_required
def user_favourites(request):
    favourites_profiles = UserFavoriteProfile.objects.filter(user=request.user)
    subscribe_to_profiles_ids = UserFavoriteProfile.objects.filter(user=request.user).values_list('profile_id',
                                                                                                  flat=True)
    subscribe_to_events_ids = []
    for event in UserFavoriteEvent.objects.filter(user=request.user):
        subscribe_to_events_ids.append(event.event_api_id or event.event_inner_id)

    subscribe_to_api_events_ids = []
    subscribe_to_inner_events_ids = []
    for event in UserFavoriteEvent.objects.filter(user=request.user):
        if event.event_api_id:
            subscribe_to_api_events_ids.append(event.event_api_id)
        elif event.event_inner_id:
            subscribe_to_inner_events_ids.append(event.event_inner_id)

    events_api = EventAPI.objects.filter(id__in=subscribe_to_api_events_ids)
    events_inner = EventInner.objects.filter(id__in=subscribe_to_inner_events_ids)

    favourites_events = list(events_api) + list(events_inner)
    return render(request, 'users/favourites.html', {'favourites_events': favourites_events,
                                                     'favourites_profiles': favourites_profiles,
                                                     'subscribe_to_profiles_ids': subscribe_to_profiles_ids,
                                                     'subscribe_to_events_ids': subscribe_to_events_ids})
