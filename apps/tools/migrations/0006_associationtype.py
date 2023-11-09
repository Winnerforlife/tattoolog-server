# Generated by Django 4.2.4 on 2023-11-02 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0005_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssociationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Association name')),
                ('link', models.URLField(blank=True, null=True, verbose_name='Association link')),
            ],
        ),
    ]
