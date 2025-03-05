from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Course, Blog, Leads, ContactMessage, BusinessLeads, CourseRegistration, Class, SignUp #, Instructor, Student,
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'slug', 'course_image', 'course_content', 'description', 'you_will_learn_list', 'lessons', 'prerequisites', 'category', 'duration', 'language', 'skill_level', 'price', 'orignal_price', 'last_updated', 'tags', 'is_featured', 'faq', 'meta_title', 'meta_description', 'Canonical_tag', 'buy_button_id']


# class InstructorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Instructor
#         fields = ['id', 'name', 'phone', 'email', 'rate', 'address', 'skill_set']

class BusinessLeadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessLeads
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leads
        fields = '__all__'

class PaymentSerializer(serializers.Serializer):
    user_email = serializers.EmailField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=10)


class CourseRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRegistration
        fields = ['email', 'course_name']


# class StudentSerializer(serializers.ModelSerializer):
#     payment_status = serializers.SerializerMethodField()

#     class Meta:
#         model = Student
#         fields = ['id', 'first_name', 'last_name', 'email_id', 'address', 'phone_number', 'alternative_phone_number', 'alternative_email', 'company', 'experience', 'student_image', 'payment_status']

#     def get_payment_status(self, obj):
#         lead = Leads.objects.filter(email=obj.email_id).first()
#         return lead.payment_status if lead else False

# class ClassSerializer(serializers.ModelSerializer):
#     students = serializers.SerializerMethodField()
#     instructor = serializers.SerializerMethodField()
#     course = serializers.SerializerMethodField()
#     student_payment_status = serializers.SerializerMethodField()

#     class Meta:
#         model = Class
#         fields = ['id', 'course', 'instructor', 'class_date', 'study_material', 'class_joining_link', 'students', 'student_payment_status']

#     def get_students(self, obj):
#         """Returns students with their names and payment status"""
#         students_data = []
#         payment_info = obj.get_student_payment_status()

#         for student in obj.students.all():
#             students_data.append({
#                 "id": student.id,
#                 "name": student.username,  # Using `username` from SignUp instead of `first_name`
#                 "email": student.email,  # SignUp uses `email` instead of `email_id`
#                 "payment_status": payment_info.get(student.email, "Not Found")  # Updated to match email field
#             })
#         return students_data

#     def get_instructor(self, obj):
#         if obj.instructor:
#             return {
#                 "id": obj.instructor.id,
#                 "name": obj.instructor.name
#             }
#         return None

#     def get_course(self, obj):
#         """Returns course details, handling the case where obj.course is None"""
#         course = obj.course
#         if course:
#             return {
#                 "id": course.id,
#                 "course_name": course.course_name,
#                 "description": course.description,
#                 "price": course.price
#             }
#         return None

#     def get_student_payment_status(self, obj):
#         """Returns the student payment status dictionary"""
#         return obj.get_student_payment_status()




# Signup Serializer
# class SignUpSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SignUp
#         fields = ["id", "username", "email", "phone_number", "password", "role", 'student_alternative_phone_number', 'student_alternative_email', 'student_company', 'student_experience', 'student_image', 'rate', 'address', 'skill_set']
#         extra_kwargs = {"password": {"write_only": True}}

#     def create(self, validated_data):
#         validated_data["password"] = make_password(validated_data["password"])  # Hash password
#         user = super().create(validated_data)

#         # Automatically create a StudentProfile if the user is a student
#         if user.role == "student":
#             StudentProfile.objects.create(user=user)
#             print(f"✅ StudentProfile created for {user.username}")

#         return user
    
    
# Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        try:
            user = SignUp.objects.get(username=username)
        except SignUp.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password")

        if not check_password(password, user.password):  # Check hashed password
            raise serializers.ValidationError("Invalid username or password")

        return user


# class SignUpSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SignUp
#         fields = '__all__'

# class ClassSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Class
#         fields = '__all__'
        
        
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignUp
        fields = ["id", "username", "email", "phone_number", "password", "role", 'student_alternative_phone_number', 'student_alternative_email', 'student_company', 'student_experience', 'student_image', 'rate', 'address', 'skill_set']  # Include only relevant fields

class ClassSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField()
    instructor = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()
    student_payment_status = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = ["id", "class_name", "class_date", "study_material", "class_joining_link", "instructor", "course", "students", "student_payment_status"]

    def get_students(self, obj):
        """Returns students with their names and payment status"""
        students_data = []
        payment_info = obj.get_student_payment_status()  # Fetch payment status from model method

        for student in obj.students.all():
            students_data.append({
                "id": student.id,
                "name": student.username,  # Using `username` from SignUp
                "email": student.email,  # Using `email` from SignUp
                "payment_status": payment_info.get(student.email, "Not Found")  # Get status by email
            })
        return students_data

    def get_instructor(self, obj):
        """Returns instructor details"""
        if obj.instructor:
            return {
                "id": obj.instructor.id,
                "name": obj.instructor.username  # Changed from `.name` to `.username`
            }
        return None

    def get_course(self, obj):
        """Returns course details, handling cases where obj.course is None"""
        if obj.course:
            return {
                "id": obj.course.id,
                "course_name": obj.course.course_name,
                "description": obj.course.description,
                "price": obj.course.price
            }
        return None

    def get_student_payment_status(self, obj):
        """Returns the student payment status dictionary"""
        return obj.get_student_payment_status()  # Calls model method for payment status
