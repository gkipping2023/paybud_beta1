# Generated by Django 4.1.5 on 2023-01-27 12:47

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aircraft_Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aircraft_type', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Logbook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('cmp_id', models.CharField(max_length=6, null=True)),
                ('route', models.CharField(max_length=250)),
                ('total_hrs_input', models.CharField(max_length=2)),
                ('total_min_input', models.CharField(max_length=2)),
                ('total_decimal', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('total_flight_block', models.CharField(blank=True, max_length=5, null=True)),
                ('sun_hrs_input', models.CharField(blank=True, default=main.models.Logbook.default_zero, max_length=2, null=True)),
                ('sun_min_input', models.CharField(blank=True, default=main.models.Logbook.default_zero, max_length=2, null=True)),
                ('total_sun_block', models.CharField(blank=True, max_length=5, null=True)),
                ('sun_decimal', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('holiday_hrs_input', models.CharField(blank=True, default=main.models.Logbook.default_zero, max_length=2, null=True)),
                ('holiday_min_input', models.CharField(blank=True, default=main.models.Logbook.default_zero, max_length=2, null=True)),
                ('total_holiday_block', models.CharField(blank=True, max_length=5, null=True)),
                ('holiday_decimal', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('libre_hrs_input', models.CharField(blank=True, default=main.models.Logbook.default_zero, max_length=2, null=True)),
                ('libre_min_input', models.CharField(blank=True, default=main.models.Logbook.default_zero, max_length=2, null=True)),
                ('total_libre_block', models.CharField(blank=True, max_length=5, null=True)),
                ('libre_decimal', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('sa_hrs_input', models.CharField(blank=True, default=main.models.Logbook.default_zero, max_length=2, null=True)),
                ('sa_min_input', models.CharField(blank=True, default=main.models.Logbook.default_zero, max_length=2, null=True)),
                ('total_sa_block', models.CharField(blank=True, max_length=5, null=True)),
                ('sa_decimal', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('remarks', models.CharField(blank=True, max_length=250, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PilotRank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pilot_position', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200, null=True)),
                ('lastname', models.CharField(max_length=200, null=True)),
                ('cm_id', models.CharField(max_length=7)),
                ('mail', models.EmailField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('cmp_id', models.CharField(max_length=20, null=True, unique=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('position', models.ForeignKey(max_length=20, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.pilotrank')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
