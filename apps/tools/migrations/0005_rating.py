# Generated by Django 4.2.4 on 2023-10-11 11:54

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_profile_count_visit'),
        ('tools', '0004_blog'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.TextField(blank=True, default='')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating_profile', to='accounts.profile')),
            ],
        ),
    ]