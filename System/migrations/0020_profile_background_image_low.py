# Generated by Django 2.2.6 on 2019-12-30 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0019_remove_profile_background_image_low'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='background_image_low',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics_background'),
        ),
    ]