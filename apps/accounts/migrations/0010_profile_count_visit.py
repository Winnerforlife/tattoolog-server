# Generated by Django 4.2.4 on 2023-09-26 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_profile_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='count_visit',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Count visit'),
        ),
    ]