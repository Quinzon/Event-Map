# Generated by Django 4.1.3 on 2023-05-05 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("map", "0002_event_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="event_images/"),
        ),
    ]