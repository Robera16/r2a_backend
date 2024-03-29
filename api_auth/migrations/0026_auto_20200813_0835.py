# Generated by Django 3.0.5 on 2020-08-13 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_auth', '0025_auto_20200805_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='phoneotp',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api_auth.Country'),
        ),
        migrations.AddField(
            model_name='phoneotp',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='phoneotp',
            unique_together={('phone_number', 'email')},
        ),
    ]
