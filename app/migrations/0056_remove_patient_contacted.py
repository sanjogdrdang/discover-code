# Generated by Django 4.1.5 on 2023-03-22 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0055_alter_patient_contacted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='contacted',
        ),
    ]
