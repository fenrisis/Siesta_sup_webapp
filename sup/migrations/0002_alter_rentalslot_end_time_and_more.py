# Generated by Django 4.2.3 on 2023-07-26 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sup', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentalslot',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rentalslot',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
