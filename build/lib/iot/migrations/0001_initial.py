# Generated by Django 2.0.1 on 2018-01-23 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IoT',
            fields=[
                ('serial_no', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('plate_no', models.CharField(blank=True, max_length=50, unique=True)),
                ('is_active', models.BooleanField()),
            ],
        ),
    ]
