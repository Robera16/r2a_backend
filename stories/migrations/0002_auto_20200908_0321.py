# Generated by Django 3.0.5 on 2020-09-08 03:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stories', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='seen_by',
            field=models.ManyToManyField(blank=True, related_name='seen_stories', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='story',
            name='story_type',
            field=models.IntegerField(blank=True, choices=[(1, 'media'), (2, 'text'), (3, 'un-supported')]),
        ),
    ]
