# Generated by Django 3.2.8 on 2023-12-20 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('to_do_app', '0003_auto_20231220_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='channel_name',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='task',
            name='channel_name',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]