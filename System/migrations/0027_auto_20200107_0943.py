# Generated by Django 2.2.6 on 2020-01-07 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0026_auto_20200107_0936'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='friendReqests',
        ),
        migrations.AddField(
            model_name='profile',
            name='from_user',
            field=models.ManyToManyField(blank=True, related_name='from_user1', to='System.Profile'),
        ),
        migrations.AddField(
            model_name='profile',
            name='to_user',
            field=models.ManyToManyField(blank=True, related_name='to_user1', to='System.Profile'),
        ),
    ]
