# Generated by Django 5.0.4 on 2024-04-29 02:46

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_remove_user_info_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Login_history',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logged_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.user_info')),
            ],
        ),
    ]
