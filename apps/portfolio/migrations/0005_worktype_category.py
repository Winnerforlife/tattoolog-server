# Generated by Django 4.2.4 on 2024-01-28 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_moderationassociation_associationphotoproof'),
    ]

    operations = [
        migrations.AddField(
            model_name='worktype',
            name='category',
            field=models.CharField(choices=[('tattoo', 'Tattoo'), ('piercing', 'Piercing')], default='tattoo', verbose_name='Work type category'),
        ),
    ]
