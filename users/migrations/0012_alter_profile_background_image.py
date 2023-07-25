# Generated by Django 4.1.3 on 2023-06-19 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0011_remove_profile_bio_profile_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="background_image",
            field=models.ImageField(
                blank=True,
                default="default_images/profile_background_image.svg",
                upload_to="profile_images/",
            ),
        ),
    ]