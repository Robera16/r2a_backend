# Generated by Django 3.0.5 on 2020-04-19 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_auth', '0005_auto_20200419_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(1, 'political_rep'), (2, 'medical_rep'), (3, 'user')], default=3),
        ),
    ]
