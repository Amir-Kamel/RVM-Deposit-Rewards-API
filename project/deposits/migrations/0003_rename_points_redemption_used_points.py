# Generated by Django 5.2.4 on 2025-07-27 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deposits', '0002_redemption'),
    ]

    operations = [
        migrations.RenameField(
            model_name='redemption',
            old_name='points',
            new_name='used_points',
        ),
    ]
