# Generated by Django 3.0.5 on 2020-04-23 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_auth', '0006_user_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='district',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='last_name',
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='banner',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='sex',
            field=models.SmallIntegerField(blank=True, choices=[(1, 'Male'), (2, 'Female'), (3, 'Trans-Sexual')], default=1),
            preserve_default=False,
        ),
    ]
