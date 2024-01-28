# Generated by Django 4.2.4 on 2024-01-28 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0017_alter_socialmedia_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Blog category name')),
            ],
        ),
        migrations.AddField(
            model_name='blogpost',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='blog_category', to='tools.blogcategory', verbose_name='Blog category'),
        ),
    ]
