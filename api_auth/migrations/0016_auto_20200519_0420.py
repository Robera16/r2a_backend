# Generated by Django 3.0.5 on 2020-05-19 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_auth', '0015_auto_20200515_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='profiles1589862026'),
        ),
    ]
