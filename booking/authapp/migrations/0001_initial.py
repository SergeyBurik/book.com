# Generated by Django 3.0.3 on 2020-03-14 08:05

import authapp.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


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
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Адрес электронной почты')),
                ('active', models.BooleanField(default=True, verbose_name='Активный')),
                ('name', models.CharField(default='', max_length=30, verbose_name='Имя')),
                ('surname', models.CharField(default='', max_length=30, verbose_name='Фамилия')),
                ('phone_number', models.CharField(default='', max_length=30, verbose_name='Номер телефона')),
                ('country', models.CharField(default='', max_length=30, verbose_name='Страна')),
                ('company_name', models.CharField(default='', max_length=30)),
                ('staff', models.BooleanField(default=False, verbose_name='Сотрудник')),
                ('admin', models.BooleanField(default=True, verbose_name='Администратор')),
                ('is_sending', models.BooleanField(default=False, verbose_name='Подписка на рассылку')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='UserSending',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Адрес электронной почты')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активна рассылка')),
            ],
            options={
                'verbose_name': 'Подписчик',
                'verbose_name_plural': 'Подписчики',
            },
        ),
        migrations.CreateModel(
            name='UserActivation',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('activation_key', models.CharField(blank=True, max_length=128)),
                ('activation_key_expires', models.DateTimeField(default=authapp.models.get_activation_key_time)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('age', models.PositiveIntegerField(blank=True, null=True, verbose_name='Возраст')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Мужской'), ('W', 'Женский')], max_length=1, verbose_name='Пол')),
                ('avatar', models.ImageField(default='static/img/default_user.png', upload_to=authapp.models.PathAndRename('static/img/tmp'), verbose_name='Изображение пользователя')),
            ],
        ),
    ]
