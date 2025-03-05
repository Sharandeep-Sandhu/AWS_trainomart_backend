from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.text import slugify
#from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.



class Course(models.Model):
    course_name = models.CharField(max_length=255)
#    slug = models.SlugField(unique=True)
    course_image = models.ImageField(upload_to='courses/')  # Ensure you have Pillow installed
    description = models.TextField(max_length=500000)
    course_content = models.TextField(max_length=500000)
    you_will_learn_list = models.TextField(max_length=500000)
    lessons = models.TextField(max_length=500000)
    category = models.CharField(max_length=255)
    prerequisites = models.TextField(max_length=500000)
    orignal_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.TextField(help_text="Enter the duration of the course")
    language = models.CharField(max_length=100)
    skill_level = models.CharField(max_length=50, choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')])
    last_updated = models.DateTimeField(auto_now=True)  # Automatically set to now every time the object is saved
    tags = models.CharField(max_length=1000, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    faq = models.TextField(max_length=500000, blank=True, null=True)
    buy_button_id = models.CharField(max_length=344, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically sets when first created
    updated_at = models.DateTimeField(auto_now=True)
    # New fields for SEO meta tags
    meta_title = models.CharField(max_length=2555, help_text="Title for SEO and social sharing", null=True, blank=True)
    meta_description = models.TextField(max_length=5000, help_text="Description for SEO and social sharing", null=True, blank=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)
    canonical_tag = models.CharField(max_length=2555, help_text="Canonical for SEO and social sharing", null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.course_name)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.course_name

    
class Blog(models.Model):
    blog_title = models.CharField(max_length=255)
    blog_image = models.ImageField(upload_to='blogs/')  # Ensure you have Pillow installed
    blog_data = models.TextField()
    category = models.CharField(max_length=255)
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta_title = models.CharField(max_length=2555, help_text="Title for SEO and social sharing", null=True, blank=True)
    meta_description = models.TextField(max_length=5000, help_text="Description for SEO and social sharing", null=True, blank=True)
    Canonical_tag = models.CharField(max_length=2555, help_text="Canonical for SEO and social sharing", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically sets when first created


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.blog_title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.blog_title


class Leads(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)  # Adjust max_length as needed
    email = models.EmailField()
    time_to_call = models.DateTimeField()
    course_name = models.CharField(max_length=1500)
    payment_status = models.BooleanField(default=False)  # True or False

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
    
class Payment(models.Model):
    payment_id = models.CharField(max_length=100, unique=True)
    user_email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_id} - {self.status}"


class BusinessLeads(models.Model):
    name = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class CourseRegistration(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255)
    course_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.email} - {self.course_name}"


class Instructor(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=255)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()
    skill_set = models.TextField()

    def __str__(self):
        return self.name

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_id = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=150)
    alternative_phone_number = models.CharField(max_length=150, blank=True, null=True)
    alternative_email = models.EmailField(blank=True, null=True)
    company = models.TextField(max_length=255, blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    student_image = models.ImageField(upload_to='student_images/', blank=True, null=True)  # ✅ Image Field Added

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class SignUp(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    ]
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=255)  # Store hashed passwords!
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    student_alternative_phone_number = models.CharField(max_length=150, blank=True, null=True)
    student_alternative_email = models.EmailField(blank=True, null=True)
    student_company = models.TextField(max_length=255, blank=True, null=True)
    student_experience = models.TextField(blank=True, null=True)
    student_image = models.ImageField(upload_to='student_images/', blank=True, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    skill_set = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} - {self.role}"

class Class(models.Model):
    class_name = models.CharField(max_length=500)
    students = models.ManyToManyField(SignUp, related_name="enrolled_classes")
    instructor = models.ForeignKey(SignUp, on_delete=models.CASCADE, related_name='classes', blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='classes', blank=True, null=True)
    class_date = models.DateTimeField(blank=True, null=True)
    study_material = models.FileField(upload_to='study_materials/', blank=True, null=True)
    class_joining_link = models.URLField(blank=True, null=True)

    def get_student_payment_status(self):
        """Check payment status of all students in this class based on Leads table."""
        payment_info = {}
        for student in self.students.all():
            # Use student.email instead of student.email_id (since SignUp model has 'email' field)
            lead = Leads.objects.filter(email=student.email, course_name=self.course.course_name).first()
            payment_info[student.email] = lead.payment_status if lead else False
        return payment_info


    def __str__(self):
        return f"{self.course} | {self.class_date}"
