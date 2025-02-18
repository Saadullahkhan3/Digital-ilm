# Generated by Django 5.1.2 on 2025-02-18 17:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0015_remove_questionsheet_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionsheet',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionsheet',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
