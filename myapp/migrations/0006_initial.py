# Generated by Django 4.2.4 on 2023-08-26 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('myapp', '0005_delete_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=35)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('added_to', models.DateTimeField(auto_now_add=True)),
                ('is_approved', models.BooleanField(default=True)),
            ],
        ),
    ]
