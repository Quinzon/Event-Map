# Generated by Django 4.1.3 on 2023-05-15 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("map", "0011_alter_eventapi_description_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventapi",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="eventinner",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]