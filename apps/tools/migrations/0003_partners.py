# Generated by Django 4.2.4 on 2023-09-25 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0002_alter_socialmedia_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Partner name')),
                ('logo', models.ImageField(upload_to='partners/logo', verbose_name='Logo')),
                ('link', models.URLField(blank=True, null=True, verbose_name='Partner link')),
            ],
        ),
    ]
