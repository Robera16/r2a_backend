# Generated by Django 3.0.5 on 2020-08-25 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20200730_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='file_type',
            field=models.IntegerField(choices=[(1, 'IMG'), (2, 'VID'), (3, 'OTHER')], default=1),
            preserve_default=False,
        ),
    ]
