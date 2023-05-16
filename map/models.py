from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    link = models.URLField(max_length=500, null=True, blank=True)
    image = models.ImageField(max_length=500, upload_to='event_images/', null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "address": self.address if self.address else None,
            "location": self.location,
            "date": self.date.isoformat() if self.date else None,
            "link": self.link,
            "image_url": self.image.url if self.image else None,
        }


class EventInner(Event):
    pass


class EventAPI(Event):
    image = models.URLField(max_length=500, null=True, blank=True)
    full_description = models.TextField(null=True, blank=True)

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "address": self.address if self.address else None,
            "location": self.location,
            "date": self.date.isoformat() if self.date else None,
            "link": self.link,
            "image_url": self.image if self.image else None,
        }
