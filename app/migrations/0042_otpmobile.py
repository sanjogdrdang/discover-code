# Generated by Django 4.1.5 on 2023-02-22 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0041_test_test_link_test_test_reason'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtpMobile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=180)),
                ('otp', models.CharField(max_length=180)),
                ('verified', models.BooleanField(default=False)),
            ],
        ),
    ]
