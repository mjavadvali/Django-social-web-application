# Generated by Django 5.1 on 2024-09-08 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_post_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
    ]
