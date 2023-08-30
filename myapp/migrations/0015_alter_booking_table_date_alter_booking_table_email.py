# Generated by Django 4.2.4 on 2023-08-27 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_booking_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking_table',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='booking_table',
            name='email',
            field=models.EmailField(max_length=30),
        ),
    ]
