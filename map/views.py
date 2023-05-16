from django.shortcuts import render, get_object_or_404
from .models import EventInner, EventAPI
from itertools import chain
from django.http import Http404
import json
import keys


def get_events(request):
    event_inner_queryset = EventInner.objects.all()
    event_api_queryset = EventAPI.objects.all()

    events = list(chain(event_inner_queryset, event_api_queryset))
    events_json = json.dumps([event.as_dict() for event in events])

    return render(request, "map/home.html", {"events_json": events_json, "Yandex_API": keys.Keys.Yandex_API})


def event_detail(request, event_id):
    try:
        event = EventAPI.objects.get(id=event_id)
    except EventAPI.DoesNotExist:
        try:
            event = EventInner.objects.get(id=event_id)
        except EventInner.DoesNotExist:
            raise Http404("Event does not exist")
    return render(request, 'map/event.html', {'event': event})
