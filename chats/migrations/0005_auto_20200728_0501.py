# Generated by Django 3.0.5 on 2020-07-28 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0004_auto_20200621_0700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='attachments/group_pictures'),
        ),
    ]
