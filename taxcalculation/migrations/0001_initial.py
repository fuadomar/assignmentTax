# Generated by Django 2.1.2 on 2018-10-29 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.FileField(upload_to='uploads/%Y/%m/%d/')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=15)),
                ('fest_bonus', models.IntegerField()),
                ('pf', models.IntegerField()),
                ('total_income', models.IntegerField()),
                ('emp_id', models.CharField(blank=True, max_length=25, null=True)),
                ('department', models.CharField(blank=True, max_length=25, null=True)),
                ('designation', models.CharField(blank=True, max_length=25, null=True)),
                ('joining_date', models.CharField(blank=True, max_length=25, null=True)),
                ('income_year', models.CharField(blank=True, max_length=25, null=True)),
                ('assessment_year', models.CharField(blank=True, max_length=25, null=True)),
                ('investment_made', models.IntegerField()),
                ('tax_deducted_by_nascenia', models.IntegerField()),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='persons', to='taxcalculation.File')),
            ],
        ),
    ]
