# Generated by Django 4.1.3 on 2022-11-22 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0013_alter_details_cancel_remarks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='details',
            name='cancel_remarks',
            field=models.CharField(max_length=500, null=True),
        ),
    ]