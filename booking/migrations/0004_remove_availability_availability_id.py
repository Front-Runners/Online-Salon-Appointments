# Generated by Django 4.1.3 on 2022-11-18 21:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_alter_availability_is_available'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='availability',
            name='availability_id',
        ),
    ]