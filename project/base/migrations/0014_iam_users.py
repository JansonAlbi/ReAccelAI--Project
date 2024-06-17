# Generated by Django 5.0.3 on 2024-06-15 19:08

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_uploadedfile_model_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='iam_users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reaccel_id', models.CharField(max_length=100)),
                ('iam_user_name', models.CharField(max_length=100)),
                ('iam_user_password', models.CharField(max_length=255)),
                ('access_permissions', models.CharField(max_length=255)),
                ('user_createdon', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]