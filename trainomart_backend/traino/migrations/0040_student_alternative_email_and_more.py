# Generated by Django 5.1.1 on 2025-02-25 09:38

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traino', '0039_remove_signup_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='alternative_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='alternative_phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='company',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='experience',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='phone_number',
            field=models.CharField(default=django.utils.timezone.now, max_length=15),
            preserve_default=False,
        ),
    ]
