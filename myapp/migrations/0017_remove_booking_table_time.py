# Generated by Django 4.2.4 on 2023-08-27 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_alter_booking_table_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking_table',
            name='time',
        ),
    ]