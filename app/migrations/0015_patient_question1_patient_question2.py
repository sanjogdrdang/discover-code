# Generated by Django 4.1.3 on 2022-12-19 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_patient_subgoal'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='question1',
            field=models.CharField(default='none', max_length=100),
        ),
        migrations.AddField(
            model_name='patient',
            name='question2',
            field=models.CharField(default='none', max_length=100),
        ),
    ]
