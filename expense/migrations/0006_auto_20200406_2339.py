# Generated by Django 2.2.4 on 2020-04-06 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0005_auto_20200406_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='pay_type',
            field=models.CharField(max_length=50),
        ),
    ]