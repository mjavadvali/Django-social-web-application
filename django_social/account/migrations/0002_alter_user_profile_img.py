# Generated by Django 5.1 on 2024-08-27 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_img',
            field=models.ImageField(default='/profile_images/avatar.png', upload_to='profile_images'),
        ),
    ]
