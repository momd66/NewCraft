# Generated by Django 2.2.6 on 2019-12-30 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0022_auto_20191230_0541'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='youtube',
            field=models.URLField(blank=True, null=True),
        ),
    ]