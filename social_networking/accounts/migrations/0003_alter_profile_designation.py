# Generated by Django 5.0.3 on 2024-03-30 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_profile_interest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='designation',
            field=models.CharField(blank=True, default='Unspecified', max_length=256, null=True),
        ),
    ]
