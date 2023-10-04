# Generated by Django 3.0.5 on 2020-04-12 09:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                ('active', models.BooleanField(default=True)),
                ('phone_number', models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator(code='invalid phone_number', message='phone_number must be 10-15  digits long', regex='^\\+?1?\\d{9,15}$')])),
                ('age', models.IntegerField()),
                ('otp', models.CharField(default='', max_length=5)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('medical_rep', models.BooleanField(default=False)),
                ('political_rep', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PhoneOtp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator(code='invalid phone_number', message='phone_number must be 10-15  digits long', regex='^\\+?1?\\d{9,15}$')])),
                ('otp', models.CharField(max_length=5)),
                ('attempts', models.IntegerField(default=0)),
                ('validated', models.BooleanField(default=False)),
            ],
        ),
    ]
