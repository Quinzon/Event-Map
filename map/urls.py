from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_events, name='home'),
    path('event/<str:event_id>/', views.event_detail, name='event_detail'),
    path('toggle_event_subscription/', views.toggle_event_subscription, name='toggle_event_subscription'),
]
