# Generated by Django 3.0.5 on 2020-05-15 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_auth', '0014_user_can_create'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
