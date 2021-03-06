# Generated by Django 2.2.4 on 2020-04-06 18:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0004_auto_20200406_2215'),
    ]

    operations = [
        migrations.RenameField(
            model_name='income',
            old_name='type',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='income',
            old_name='amt',
            new_name='spent',
        ),
        migrations.AddField(
            model_name='income',
            name='pay_type',
            field=models.CharField(default='net banking', max_length=50),
        ),
        migrations.AddField(
            model_name='income',
            name='recursive',
            field=models.BooleanField(default=False, max_length=100),
        ),
        migrations.AddField(
            model_name='income',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='income',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
