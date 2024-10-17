# Generated by Django 5.1 on 2024-10-08 13:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_remove_user_follows_userfollowing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfollowing',
            name='followed_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_by', to=settings.AUTH_USER_MODEL),
        ),
    ]