# Generated by Django 5.1.2 on 2025-02-18 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0013_questionsheet_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionsheet',
            name='attempted_count',
        ),
    ]
