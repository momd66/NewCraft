# Generated by Django 2.2.6 on 2019-12-27 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0013_profile_background_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='facebock',
            field=models.URLField(blank=True, null=True),
        ),
    ]
