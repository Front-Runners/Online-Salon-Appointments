# Generated by Django 4.1.3 on 2022-11-18 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('availability_id', models.IntegerField()),
                ('slot_start', models.DateTimeField()),
                ('slot_end', models.DateTimeField()),
                ('is_available', models.SmallIntegerField()),
            ],
            options={
                'ordering': ['slot_start'],
            },
        ),
    ]