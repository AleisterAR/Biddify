# Generated by Django 5.0.6 on 2024-09-06 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0002_alter_participant_managers_participant_firstname_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='lastname',
        ),
    ]
