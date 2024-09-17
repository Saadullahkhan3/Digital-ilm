# Generated by Django 5.1.1 on 2024-09-16 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionsheet',
            name='level',
            field=models.CharField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default='yes', max_length=1),
            preserve_default=False,
        ),
    ]