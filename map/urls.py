from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_events, name='home'),
    path('event', views.event, name='event'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
]
