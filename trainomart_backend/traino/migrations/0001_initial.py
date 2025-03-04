# Generated by Django 5.1.1 on 2025-02-27 11:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_title', models.CharField(max_length=255)),
                ('blog_image', models.ImageField(upload_to='blogs/')),
                ('blog_data', models.TextField()),
                ('category', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, unique=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('meta_title', models.CharField(blank=True, help_text='Title for SEO and social sharing', max_length=2555, null=True)),
                ('meta_description', models.TextField(blank=True, help_text='Description for SEO and social sharing', max_length=5000, null=True)),
                ('Canonical_tag', models.CharField(blank=True, help_text='Canonical for SEO and social sharing', max_length=2555, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessLeads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('organization', models.CharField(max_length=100)),
                ('designation', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=255)),
                ('course_image', models.ImageField(upload_to='courses/')),
                ('description', models.TextField(max_length=500000)),
                ('course_content', models.TextField(max_length=500000)),
                ('you_will_learn_list', models.TextField(max_length=500000)),
                ('lessons', models.TextField(max_length=500000)),
                ('category', models.CharField(max_length=255)),
                ('prerequisites', models.TextField(max_length=500000)),
                ('orignal_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('duration', models.TextField(help_text='Enter the duration of the course')),
                ('language', models.CharField(max_length=100)),
                ('skill_level', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], max_length=50)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('tags', models.CharField(blank=True, max_length=1000, null=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('faq', models.TextField(blank=True, max_length=500000, null=True)),
                ('buy_button_id', models.CharField(blank=True, max_length=344, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('meta_title', models.CharField(blank=True, help_text='Title for SEO and social sharing', max_length=2555, null=True)),
                ('meta_description', models.TextField(blank=True, help_text='Description for SEO and social sharing', max_length=5000, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseRegistration',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255)),
                ('course_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=255)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('address', models.TextField()),
                ('skill_set', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Leads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('time_to_call', models.DateTimeField()),
                ('course_name', models.CharField(max_length=1500)),
                ('payment_status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=100, unique=True)),
                ('user_email', models.EmailField(max_length=254)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SignUp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=255)),
                ('role', models.CharField(choices=[('student', 'Student'), ('instructor', 'Instructor'), ('admin', 'Admin')], default='student', max_length=20)),
                ('student_alternative_phone_number', models.CharField(blank=True, max_length=150, null=True)),
                ('student_alternative_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('student_company', models.TextField(blank=True, max_length=255, null=True)),
                ('student_experience', models.TextField(blank=True, null=True)),
                ('student_image', models.ImageField(blank=True, null=True, upload_to='student_images/')),
                ('rate', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('skill_set', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email_id', models.EmailField(max_length=254, unique=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('phone_number', models.CharField(max_length=150)),
                ('alternative_phone_number', models.CharField(blank=True, max_length=150, null=True)),
                ('alternative_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('company', models.TextField(blank=True, max_length=255, null=True)),
                ('experience', models.TextField(blank=True, null=True)),
                ('student_image', models.ImageField(blank=True, null=True, upload_to='student_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_date', models.DateTimeField(blank=True, null=True)),
                ('study_material', models.FileField(blank=True, null=True, upload_to='study_materials/')),
                ('class_joining_link', models.URLField(blank=True, null=True)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='traino.course')),
                ('instructor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='traino.signup')),
                ('students', models.ManyToManyField(related_name='enrolled_classes', to='traino.signup')),
            ],
        ),
    ]
