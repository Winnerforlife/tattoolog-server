# Generated by Django 4.2.4 on 2023-09-18 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_profile_city_profile_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='Birthday'),
        ),
    ]
