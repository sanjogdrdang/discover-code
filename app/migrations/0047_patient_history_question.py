# Generated by Django 4.1.5 on 2023-03-15 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0046_alter_patient_history_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='history_question',
            field=models.CharField(default='none', max_length=200),
        ),
    ]
