# Generated by Django 2.2.4 on 2020-04-07 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0008_month_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='month_link',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='expense.Month'),
        ),
    ]
