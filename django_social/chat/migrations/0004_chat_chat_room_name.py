# Generated by Django 5.1.2 on 2024-10-18 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_message_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='chat_room_name',
            field=models.CharField(blank=True, max_length=550),
        ),
    ]
