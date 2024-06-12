# Generated by Django 5.0.3 on 2024-06-12 07:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_otp'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reaccel_id', models.EmailField(max_length=254)),
                ('project_name', models.CharField(max_length=100)),
                ('class_names', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='uploads/')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('epoch_value', models.IntegerField()),
                ('batch_size', models.IntegerField()),
                ('learning_rate', models.IntegerField()),
                ('project_status', models.IntegerField()),
            ],
        ),
    ]
