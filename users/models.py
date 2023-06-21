from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from map.models import EventInner, EventAPI


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', default='default_images/anonymous.svg', blank=True)
    background_image = models.ImageField(upload_to='profile_images/',
                                         default='default_images/profile_background_image.svg', blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    status = models.TextField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class UserFavoriteEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_inner = models.ForeignKey(EventInner, on_delete=models.CASCADE, null=True, blank=True)
    event_api = models.ForeignKey(EventAPI, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class UserFavoriteProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
