# Generated by Django 5.0.3 on 2024-04-02 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpost',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
