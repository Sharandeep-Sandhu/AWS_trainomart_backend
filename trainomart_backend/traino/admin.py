from django.contrib import admin
from .models import Course, Blog, Leads, ContactMessage, BusinessLeads, CourseRegistration, Class, SignUp #, Instructor, Student
from django.contrib.auth.admin import UserAdmin

class SignUpAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone_number', 'role', 'student_alternative_phone_number', 'student_alternative_email', 'student_company', 'student_experience', 'student_image', 'rate', 'address', 'skill_set')  # Columns to show
    search_fields = ('username', 'email', 'phone_number')  # Enable search
    list_filter = ('role',)  # Filter by role
    ordering = ('id',)  # Order by ID

# @admin.register(Instructor)
# class InstructorAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'phone', 'rate')  # Display these fields in the list view
#     search_fields = ('name', 'email', 'phone')  # Enable search functionality
#     list_filter = ('rate',) 


# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'first_name', 'last_name', 'email_id', 'phone_number', 'alternative_phone_number', 'alternative_email', 'company', 'experience', 'student_image', 'address')
#     search_fields = ('first_name', 'last_name', 'email_id')


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'class_name', 'course', 'instructor', 'class_date', 'class_joining_link', 'display_student_payment_status')
    filter_horizontal = ('students',)  # Enables multi-selection for students in admin
    search_fields = ('course__course_name', 'instructor__name', 'students__first_name', 'students__email_id')
    list_filter = ('class_date', 'course')

    def display_student_payment_status(self, obj):
        """Display payment status for students in the class."""
        return obj.get_student_payment_status()
    display_student_payment_status.short_description = "Student Payment Status"

class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'category', 'orignal_price', 'price', 'Canonical_tag', 'duration', 'is_featured', 'tags', 'last_updated', 'meta_title', 'meta_description', 'slug', 'buy_button_id')
    list_filter = ('is_featured', 'language', 'skill_level')
    search_fields = ('course_name', 'description', 'slug')
    ordering = ('last_updated',)
    fields = (
        'course_name',
	    'slug',
        'course_image',
        'description',
        'course_content',
        'you_will_learn_list',  # Update this line
        'lessons',
        'prerequisites',
        'category',
        'price',
        'orignal_price',
        'duration',
        'language',
        'skill_level',
        'tags',
        'is_featured',
        'faq',
        'meta_title',
        'meta_description',
        'buy_button_id',
    )

class BlogAdmin(admin.ModelAdmin):
    list_display = ('blog_title', 'updated_at', 'blog_image', 'category', 'slug', 'meta_title', 'meta_description', 'created_at', 'Canonical_tag')
    search_fields = ('blog_title', 'category')
    ordering = ('blog_title','updated_at')
    fields = ('blog_title', 'slug', 'blog_image', 'category', 'blog_data', 'meta_title', 'meta_description', 'created_at', 'Canonical_tag')

@admin.register(BusinessLeads)
class BusinessLeadsAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'email', 'phone_number')


class StudentsAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'student_mail', 'student_phone')
    search_fields = ('student_name',)
    ordering = ('student_name',)
    fields = ('student_name', 'student_mail', 'student_phone')
class LeadsAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'time_to_call', 'course_name', 'payment_status')
    list_filter = ('payment_status',)
    search_fields = ('name', 'email')
    ordering = ('name',)
    fields = ('name', 'phone_number', 'email', 'time_to_call', 'course_name', 'payment_status')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')  # Fields to display in the list view
    search_fields = ('name', 'email')  # Fields to enable searching
    list_filter = ('created_at',)  # Enable filtering by created date
    ordering = ('-created_at',)  # Order by created date descending

@admin.register(CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'course_name')
    search_fields = ('email', 'course_name')
    list_filter = ('course_name',)


# Register the models with their corresponding admin classes
admin.site.register(Course, CourseAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Leads, LeadsAdmin)
#admin.site.register(Students, StudentsAdmin)
#admin.site.register(CourseRegistration, CourseRegistrationAdmin)
admin.site.register(SignUp, SignUpAdmin)

if not admin.site.is_registered(CourseRegistration):
    admin.site.register(CourseRegistration, CourseRegistrationAdmin)
