from django.shortcuts import render
from .models import EventInner, EventAPI
from itertools import chain
from django.http import Http404
import json
import keys
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from users.models import UserFavoriteEvent
from django.contrib.auth.models import User


def get_events(request):
    event_inner_queryset = EventInner.objects.all()
    event_api_queryset = EventAPI.objects.all()

    events = list(chain(event_inner_queryset, event_api_queryset))
    events_json = json.dumps([event.as_dict() for event in events])

    return render(request, "map/home.html", {"events_json": events_json, "Yandex_API": keys.Keys.Yandex_API})


def event_detail(request, event_id):
    try:
        event = EventAPI.objects.get(id=event_id)
    except (EventAPI.DoesNotExist, ValueError):
        try:
            event = EventInner.objects.get(id=event_id)
            event.image = event.image.url
        except EventInner.DoesNotExist:
            raise Http404("Event does not exist")
    is_inner_event = isinstance(event, EventInner)
    if request.user.is_authenticated:
        if is_inner_event:
            is_subscribed = UserFavoriteEvent.objects.filter(user=request.user, event_inner_id=event_id).exists()
        else:
            is_subscribed = UserFavoriteEvent.objects.filter(user=request.user, event_api_id=event_id).exists()
    else:
        is_subscribed = False
    return render(request, 'map/event.html', {'event': event,
                                              'is_inner_event': is_inner_event,
                                              'is_subscribed': is_subscribed})


@csrf_exempt
def toggle_event_subscription(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        event_inner_id = request.POST.get('event_inner_id')
        event_api_id = request.POST.get('event_api_id')

        user = User.objects.get(id=user_id)

        if event_inner_id:
            event = EventInner.objects.get(id=event_inner_id)
            subscription, created = UserFavoriteEvent.objects.get_or_create(user=user, event_inner=event)
        else:
            event = EventAPI.objects.get(id=event_api_id)
            subscription, created = UserFavoriteEvent.objects.get_or_create(user=user, event_api=event)

        if not created:
            subscription.delete()
            return JsonResponse({'subscribed': False})

        return JsonResponse({'subscribed': True})
