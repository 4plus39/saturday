# Generated by Django 4.2 on 2025-04-10 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitorip',
            name='ip_address',
            field=models.GenericIPAddressField(unique=True),
        ),
    ]
