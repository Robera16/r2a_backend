# Generated by Django 3.0.5 on 2020-05-22 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_auth', '0016_auto_20200519_0420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='age',
        ),
    ]
