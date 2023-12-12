# Generated by Django 4.2.4 on 2023-12-12 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_alter_customuser_email_alter_customuser_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='profile',
            name='mentor',
            field=models.BooleanField(default=False, verbose_name='Mentor'),
        ),
        migrations.AddField(
            model_name='profile',
            name='open_to_work',
            field=models.BooleanField(default=False, verbose_name='Open to work'),
        ),
        migrations.AddField(
            model_name='profile',
            name='relocate',
            field=models.BooleanField(default=False, verbose_name='Ready to relocate'),
        ),
    ]
