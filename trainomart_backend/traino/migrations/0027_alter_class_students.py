# Generated by Django 5.1.1 on 2025-02-10 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traino', '0026_remove_class_student_class_students_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='students',
            field=models.ManyToManyField(blank=True, null=True, related_name='classes', to='traino.student'),
        ),
    ]
