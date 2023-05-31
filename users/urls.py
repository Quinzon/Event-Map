from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('create_event/', views.create_event, name='create_event'),
    path('profile/<int:user_id>/', views.profile_user, name='profile'),
    path('profile/edit/', views.profile_update, name='profile-edit'),
    path('toggle_profile_subscription/', views.toggle_profile_subscription, name='toggle_profile_subscription'),
    path('favourites/', views.user_favourites, name='favourites'),
]
