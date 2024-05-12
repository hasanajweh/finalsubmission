# Generated by Django 5.0.3 on 2024-04-24 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='available_spots',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='course',
            name='prerequisites',
            field=models.TextField(blank=True, null=True),
        ),
    ]