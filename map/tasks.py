import requests
from celery import shared_task
from .models import Event


@shared_task
def update_events():
    # Получите данные о мероприятиях с использованием API сервисов
    # Запишите полученные данные в базу данных с использованием модели Event

    events_data = requests.get("https://api.example.com/events")

    for event in events_data.json():
        Event.objects.create(
            title=event["title"],
            description=event["description"],
            location=event["location"],
            date=event["date"],
            link=event["link"],
        )
