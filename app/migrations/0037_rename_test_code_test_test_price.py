# Generated by Django 4.1.5 on 2023-01-25 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_patient_specificanswer4_patient_specificquestion4'),
    ]

    operations = [
        migrations.RenameField(
            model_name='test',
            old_name='test_code',
            new_name='test_price',
        ),
    ]
