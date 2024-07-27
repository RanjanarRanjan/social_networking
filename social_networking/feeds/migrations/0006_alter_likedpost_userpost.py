# Generated by Django 5.0.3 on 2024-05-13 08:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0005_likedpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likedpost',
            name='userPost',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='feeds.userpost'),
        ),
    ]