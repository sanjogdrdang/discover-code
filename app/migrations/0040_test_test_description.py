# Generated by Django 4.1.5 on 2023-02-11 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0039_alter_patient_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='test_description',
            field=models.CharField(default='non', max_length=500),
        ),
    ]
