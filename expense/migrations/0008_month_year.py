# Generated by Django 2.2.4 on 2020-04-07 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0007_auto_20200406_2347'),
    ]

    operations = [
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.IntegerField()),
                ('annual_income', models.IntegerField(blank=True)),
                ('annual_expenditure', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('monthly_income', models.IntegerField(blank=True)),
                ('monthy_expenditure', models.IntegerField(blank=True)),
                ('year_link', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='expense.Year')),
            ],
        ),
    ]
