# Generated by Django 3.0.5 on 2021-01-10 13:48

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0023_savedposts'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SavedPosts',
            new_name='SavedPost',
        ),
    ]
