# Generated by Django 3.0.5 on 2020-09-08 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0003_story_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='story_type',
            field=models.IntegerField(choices=[(1, 'media'), (2, 'text'), (3, 'un-supported')]),
        ),
    ]
