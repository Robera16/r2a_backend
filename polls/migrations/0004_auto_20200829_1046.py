# Generated by Django 3.0.5 on 2020-08-29 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_pollcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='pollcomment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='pollcomment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
