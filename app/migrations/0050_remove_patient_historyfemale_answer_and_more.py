# Generated by Django 4.1.5 on 2023-03-15 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0049_patient_historyfemale_answer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='historyfemale_answer',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='historyfemale_question',
        ),
    ]
