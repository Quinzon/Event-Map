from django.shortcuts import render
from .models import EventInner, EventAPI
from itertools import chain
import json
import keys


def get_events(request):
    event_inner_queryset = EventInner.objects.all()
    event_api_queryset = EventAPI.objects.all()

    events = list(chain(event_inner_queryset, event_api_queryset))
    events_json = json.dumps([event.as_dict() for event in events])

    return render(request, "map/home.html", {"events_json": events_json, "Yandex_API": keys.Keys.Yandex_API})
