# Generated by Django 3.0.5 on 2021-02-05 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20210205_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='city',
            field=models.CharField(default='HYD', max_length=200),
            preserve_default=False,
        ),
    ]
