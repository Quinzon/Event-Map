# Generated by Django 4.1.3 on 2023-05-09 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("map", "0008_alter_event_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="address",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]