# Generated by Django 2.2.4 on 2020-04-06 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0006_auto_20200406_2339'),
    ]

    operations = [
        migrations.RenameField(
            model_name='income',
            old_name='spent',
            new_name='amt',
        ),
    ]
