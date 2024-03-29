# Generated by Django 4.1.3 on 2023-06-19 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("map", "0015_alter_eventinner_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventinner",
            name="image",
            field=models.ImageField(
                blank=True,
                default="default_images/event_image.svg",
                max_length=500,
                null=True,
                upload_to="event_images/",
            ),
        ),
    ]
