# Generated by Django 4.1.5 on 2023-10-28 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_user_custom_disc_1_name_user_custom_disc_2_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='logbook',
            name='incentive',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
