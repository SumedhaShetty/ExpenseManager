# Generated by Django 2.2.4 on 2020-04-11 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0010_auto_20200411_1233'),
    ]

    operations = [
        migrations.RenameField(
            model_name='month',
            old_name='monthy_expenditure',
            new_name='monthly_expenditure',
        ),
    ]
