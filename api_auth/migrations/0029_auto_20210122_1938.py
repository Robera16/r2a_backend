# Generated by Django 3.0.5 on 2021-01-22 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_auth', '0028_remove_user_constituency_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='USERNAME', max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='phoneotp',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='phoneotp',
            name='email',
        ),
    ]
