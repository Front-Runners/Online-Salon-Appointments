# Generated by Django 4.1.3 on 2022-11-30 22:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0022_details_practitioner_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='practitionerdetails',
            name='username',
            field=models.CharField(default=django.utils.timezone.now, max_length=150),
            preserve_default=False,
        ),
    ]
