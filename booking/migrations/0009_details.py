# Generated by Django 4.1.3 on 2022-11-20 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0008_alter_availability_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateTimeField(null=True)),
                ('username', models.CharField(max_length=150)),
            ],
            options={
                'ordering': ['booking_date'],
            },
        ),
    ]
