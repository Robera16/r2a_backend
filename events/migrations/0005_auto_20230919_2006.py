# Generated by Django 3.0.5 on 2023-09-19 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20210206_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='banner',
            field=models.FileField(blank=True, upload_to='attechment'),
        ),
    ]
