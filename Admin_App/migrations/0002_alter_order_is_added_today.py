# Generated by Django 4.0.5 on 2022-07-21 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_App', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='is_added_today',
            field=models.BooleanField(default=False),
        ),
    ]
