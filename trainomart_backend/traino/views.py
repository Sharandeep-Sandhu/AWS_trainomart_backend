from django.contrib.auth.hashers import check_password
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.http import HttpResponse
#from .serializers import CourseSerializer, BlogSerializer, LeadSerializer, ContactMessageSerializer, PaymentSerializer, BusinessLeadsSerializer, CourseRegistrationSerializer, InstructorSerializer, StudentSerializer, ClassSerializer, SignUpSerializer, LoginSerializer
from .serializers import CourseSerializer, BlogSerializer, LeadSerializer, ContactMessageSerializer, PaymentSerializer, BusinessLeadsSerializer, CourseRegistrationSerializer, ClassSerializer, SignUpSerializer, LoginSerializer #, InstructorSerializer, StudentSerializer
from rest_framework.authtoken.views import ObtainAuthToken
import secrets
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

#from .models import Course, Blog, Leads, ContactMessage, Payment, BusinessLeads, CourseRegistration, Instructor, Student, Class, SignUp
from .models import Course, Blog, Leads, ContactMessage, Payment, BusinessLeads, CourseRegistration, Class, SignUp #, Instructor, Student

from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework.decorators import api_view
from rest_framework import mixins
from urllib.parse import unquote
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.utils import timezone
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.timezone import now, timedelta
from django.http import JsonResponse
from .permissions import IsStudent, IsInstructor, IsAdmin
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework import generics
from django.contrib.auth import login, logout
from django.middleware.csrf import get_token


# Create your views here.


def get_csrf_token(request):
    csrf_token = get_token(request)
    response = JsonResponse({"csrf_token": csrf_token})
    response.set_cookie("csrftoken", csrf_token, secure=True, httponly=False, samesite="None")
    return response

@api_view(['GET'])
@permission_classes([AllowAny])
def student_profile(request):
    print("data", request.user)

    """Fetch the profile of the logged-in student."""
    try:
        signup_user = get_object_or_404(SignUp, email=request.user.email)

        # Ensure student profile exists
        if not signup_user.student_profile:
            signup_user.student_profile = StudentProfile.objects.create(user=signup_user)
            print("✅ Created missing student profile:", signup_user.student_profile)

        serializer = StudentSerializer(signup_user.student_profile)
        return Response(serializer.data)

    except Exception as e:
        return Response({"error": str(e)}, status=400)



@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_data(request):
    # Count total instructors from SignUp table
    total_instructors = SignUp.objects.filter(role='instructor').count()
    
    # Count total students from SignUp table
    students_enrolled = SignUp.objects.filter(role='student').count()
    
    # Count total classes
    total_classes = Class.objects.count()
    
    return JsonResponse({
        "total_instructors": total_instructors,
        "total_classes": total_classes,
        "students_enrolled": students_enrolled
    })

class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "id": user.id,
                "username": user.username,
                "role": getattr(user, "role", "student")  # Default role if missing
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@permission_classes([AllowAny])
class UserListView(APIView):
    def get(self, request):
        users = SignUp.objects.all()  # ✅ Get all users
        serializer = SignUpSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RetrieveUserView(APIView):
    permission_classes = [AllowAny]

    """ Get user by ID """
    def get(self, request, user_id):
        user = get_object_or_404(SignUp, id=user_id)
        serializer = SignUpSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RetrieveUpdateUserView(APIView):
    permission_classes = [AllowAny]

    parser_classes = [MultiPartParser, FormParser]

    """ Get and update user by ID """
    def get(self, request, user_id):
        user = get_object_or_404(SignUp, id=user_id)
        serializer = SignUpSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        user = get_object_or_404(SignUp, id=user_id)
        serializer = SignUpSerializer(user, data=request.data, partial=True)  # Allows partial updates
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserRoleView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, user_id):  # ✅ Support PUT method
        user = get_object_or_404(SignUp, id=user_id)  
        new_role = request.data.get("role")

        if new_role not in ["admin", "student", "instructor"]:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

        user.role = new_role
        user.save()
        return Response({"message": "User role updated successfully"}, status=status.HTTP_200_OK)
    
    def patch(self, request, user_id):
        user = get_object_or_404(SignUp, id=user_id)  # ✅ Find user by ID
        new_role = request.data.get("role")

        if new_role not in ["admin", "student", "instructor"]:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

        user.role = new_role
        user.save()
        return Response({"message": "User role updated successfully"}, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            # Fetch user from the Signup table
            user = SignUp.objects.get(username=username)

            # Check if the entered password matches the stored password
            if check_password(password, user.password):  # Ensure passwords are hashed
                # Generate a random token manually
                token = secrets.token_hex(32)  # Generates a secure 64-character token
                
                # Store the token in the user's record (you need a `token` field in your model)
                user.token = token  
                user.save()

                return Response({
                    "token": token,
                    "user_id": user.id,
                    "username": user.username,
                    "role": user.role  # Ensure role is present in the Signup table
                })
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        except SignUp.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    def post(self, request):
        logout(request)  # Clear session
        response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        response.delete_cookie("sessionid")
        return response





class EnrolledClassesView(APIView):
    permission_classes = [AllowAny]

    """Get all classes enrolled by a SignUp user"""

    def get(self, request, user_id):
        print(f"View is being called for user_id: {user_id}")  # Debugging print
        signup_user = get_object_or_404(SignUp, id=user_id)

        print("signup_user ", signup_user, "-", signup_user.role)

        if signup_user.role != "student":
            return Response({"error": "User is not a student"}, status=status.HTTP_400_BAD_REQUEST)

        enrolled_classes = Class.objects.filter(students=signup_user)
        serializer = ClassSerializer(enrolled_classes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



#class ClassViewSet(viewsets.ModelViewSet):
#    permission_classes = [AllowAny]
#    queryset = Class.objects.all()
#    serializer_class = ClassSerializer
#    parser_classes = (MultiPartParser, FormParser)

#    def create(self, request, *args, **kwargs):
        """Create a new class using SignUp instead of Student."""
#        data = request.data.copy()

#        course_id = data.get("course")
#        instructor_id = data.get("instructor")

#        if not course_id or not instructor_id:
#            return Response({"error": "Course and Instructor IDs are required"}, status=status.HTTP_400_BAD_REQUEST)

#        try:
#            course = Course.objects.get(id=course_id)
#            instructor = Instructor.objects.get(id=instructor_id)
#        except (Course.DoesNotExist, Instructor.DoesNotExist) as e:
#            return Response({"error": f"Invalid course or instructor ID: {e}"}, status=status.HTTP_400_BAD_REQUEST)

#        class_instance = Class(
#            course=course,
#            instructor=instructor,
#            class_date=data.get("class_date"),
#            class_joining_link=data.get("class_joining_link"),
#        )

        # Handle students (ManyToManyField using SignUp model)
#        student_ids = [data.get(f"students[{i}]") for i in range(len(data.keys())) if f"students[{i}]" in data]

#        if student_ids:
#            students = SignUp.objects.filter(id__in=student_ids)
#            if students.count() != len(student_ids):
#                return Response({"error": "Some student IDs are invalid"}, status=status.HTTP_400_BAD_REQUEST)

#            class_instance.save()
#            class_instance.students.set(students)  # Assign students to class after saving

#        study_material = request.FILES.get('study_material')
#        if study_material:
#            class_instance.study_material = study_material

#        class_instance.save()

#        return Response({
#            "id": class_instance.id,
#            "course": class_instance.course.id,
#            "instructor": class_instance.instructor.id,
#            "class_date": class_instance.class_date,
#            "class_joining_link": class_instance.class_joining_link,
#            "students": [student.id for student in class_instance.students.all()],
#            "study_material": class_instance.study_material.url if class_instance.study_material else None,
#        }, status=status.HTTP_201_CREATED)

#    def retrieve(self, request, *args, **kwargs):
        """Get a class and show payment status for each student"""
#        instance = self.get_object()
#        serializer = self.get_serializer(instance)
#        payment_status = instance.get_student_payment_status()
#        data = serializer.data
#        data['student_payment_status'] = payment_status
#        return Response(data)

#    def update(self, request, *args, **kwargs):
        """Update class details including course, instructor, date, and students from SignUp."""
#        instance = self.get_object()
#        update_data = request.data.copy()

#        if 'course' in update_data:
#            course_data = update_data.pop('course')
#            if isinstance(course_data, list):
#                course_data = course_data[0]
#            try:
#                course = Course.objects.get(id=course_data)
#                instance.course = course
#            except Course.DoesNotExist:
#                return Response({"error": "Course not found"}, status=status.HTTP_400_BAD_REQUEST)

#        if 'instructor' in update_data:
#            instructor_data = update_data.pop('instructor')
#            if isinstance(instructor_data, list):
#                instructor_data = instructor_data[0]
#            try:
#                instructor = Instructor.objects.get(id=instructor_data)
#                instance.instructor = instructor
#            except Instructor.DoesNotExist:
#                return Response({"error": "Instructor not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Handle updating students from SignUp
#        if 'students' in update_data:
#            students_data = update_data.pop('students')
#            instance.students.clear()
#            for student_id in students_data:
#                try:
#                    student_instance = SignUp.objects.get(id=student_id)
#                    instance.students.add(student_instance)
#                except SignUp.DoesNotExist:
#                    return Response({"error": f"Student with ID {student_id} not found"}, status=status.HTTP_400_BAD_REQUEST)

#        for key, value in update_data.items():
#            setattr(instance, key, value)
#        instance.save()

#        return Response({
#            "message": "Class updated successfully",
#            "data": self.get_serializer(instance).data
#        }, status=status.HTTP_200_OK)



class StudentPaymentStatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, email):
        """Fetch payment status for a specific student using SignUp."""
        student = get_object_or_404(SignUp, email=email)
        leads = Leads.objects.filter(email=email)

        if not leads.exists():
            return Response({"message": "No lead found for this email"}, status=status.HTTP_404_NOT_FOUND)

        payment_info = {lead.course_name: lead.payment_status for lead in leads}
        return Response({"student_email": email, "payment_status": payment_info})


#class InstructorViewSet(viewsets.ModelViewSet):
#    permission_classes = [AllowAny]
#    queryset = Instructor.objects.all()
#    serializer_class = InstructorSerializer

#class InstructorCreateView(APIView):
#    permission_classes = [AllowAny]
#    def post(self, request):
#        serializer = InstructorSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#class InstructorListView(APIView):
#    permission_classes = [AllowAny]
#    def get(self, request):
#        instructors = Instructor.objects.all()
#        serializer = InstructorSerializer(instructors, many=True)
#        return Response(serializer.data)


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['course_name', 'tags']  # Allows search by course name


    def create(self, request, *args, **kwargs):
        """
        Create a new course.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the new course to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return the created course data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return errors if invalid data is provided

    @action(detail=False, methods=['get'], url_path='slug/(?P<slug>[^/.]+)')
    def get_course_by_slug(self, request, slug=None):
        print(f"Received request for slug: {slug}")  
        try:
            course = Course.objects.get(slug=slug)  # Assumes you have a 'slug' field in Course model
            serializer = self.get_serializer(course)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Filter courses by whether they are featured"""
        featured_courses = Course.objects.filter(is_featured=True)
        serializer = self.get_serializer(featured_courses, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='limited')
    def get_limited_courses(self, request):
        """Get a limited number of courses using a query parameter 'limit'"""
        print("get_limited_courses called")
        limit = request.query_params.get('limit', 8)  # Default to 8 courses
        try:
            limit = int(limit)  # Ensure the limit is an integer
        except ValueError:
            return Response({"error": "Invalid limit value"}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = Course.objects.all().order_by('-id')[:limit]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    @action(detail=True, methods=['get'], url_path='custom-get')
    def custom_get_course_by_id(self, request, pk=None):
        """Custom action to fetch course by ID"""
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    @action(detail=False, methods=['get'], url_path='by-name')
    def get_course_by_name(self, request):
        """Get course by name"""
        course_name = request.query_params.get('name', None)
        if course_name:
            # Filtering by course name
            courses = Course.objects.filter(course_name__iexact=course_name)
            if courses.exists():
                serializer = self.get_serializer(courses, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'No course name provided'}, status=status.HTTP_400_BAD_REQUEST)

    


class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BlogDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, slug, *args, **kwargs):
        try:
            blog = Blog.objects.get(slug=slug)
        except Blog.DoesNotExist:
            logger.error(f"Blog with slug '{slug}' not found.")
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BlogSerializer(blog)
        return Response(serializer.data)


class LeadViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Leads.objects.all()
    serializer_class = LeadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ContactMessageViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessLeadsViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = BusinessLeads.objects.all()
    serializer_class = BusinessLeadsSerializer

def index(request):

    return HttpResponse("Hello, world. You're at the trainomart index.")




RECAPTCHA_SECRET_KEY = '6LfSCsIqAAAAAMJ5zltPY2tAT1htkB85jxwsVUKW'  # Add your reCAPTCHA secret key here

class ContactMessageViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def create(self, request, *args, **kwargs):
        captcha_token = request.data.get("captchaToken")

        # Verify the reCAPTCHA token with Google
        captcha_response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': RECAPTCHA_SECRET_KEY,
                'response': captcha_token,
            }
        )
        captcha_data = captcha_response.json()

        if not captcha_data.get("success"):
            return Response(
                {"error": "reCAPTCHA verification failed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseRegistrationView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        registrations = CourseRegistration.objects.all()
        serializer = CourseRegistrationSerializer(registrations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def sitemap_data(request):
    permission_classes = [AllowAny]
    # Base URL for your site
    base_url = 'https://www.trainomart.com'

    # Get all courses and blogs from the database
    courses = Course.objects.all()
    blogs = Blog.objects.all()

    # Create a list for sitemap entries
    sitemap_entries = []

    # Add static routes
    sitemap_entries.append({
        'url': base_url + '/',
        'lastModified': timezone.now(),
        'priority': 1.0,
    })
    sitemap_entries.append({
        'url': base_url + '/login',
        'lastModified': timezone.now(),
        'priority': 0.8,
    })

    # Add dynamic routes for courses
    for course in courses:
        sitemap_entries.append({
            'url': f"{base_url}/courses/{course.slug}",
            'lastModified': course.updated_at,  # Assuming your Course model has an 'updated_at' field
            'priority': 0.8,
        })

    # Add dynamic routes for blogs
    for blog in blogs:
        sitemap_entries.append({
            'url': f"{base_url}/blogs/{blog.slug}",
            'lastModified': blog.updated_at,  # Assuming your Blog model has an 'updated_at' field
            'priority': 0.8,
        })

    # Generate XML sitemap content
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'

    for entry in sitemap_entries:
        xml_content += f'''
            <url>
                <loc>{entry["url"]}</loc>
                <lastmod>{entry["lastModified"].date()}</lastmod>
                <priority>{entry["priority"]}</priority>
            </url>
        '''

    xml_content += '</urlset>'

    # Return the sitemap XML response
    return HttpResponse(xml_content, content_type='application/xml')






# CRUD for SignUp Model
class SignUpCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = SignUp.objects.all()
    serializer_class = SignUpSerializer

class SignUpUpdateView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    queryset = SignUp.objects.all()
    serializer_class = SignUpSerializer
    lookup_field = 'pk'

class SignUpDeleteView(generics.DestroyAPIView):
    permission_classes = [AllowAny]
    queryset = SignUp.objects.all()
    lookup_field = 'pk'

# CRUD for Class Model
class ClassCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    def post(self, request, *args, **kwargs):
        data = request.data.copy()  # Make a mutable copy of the data
        
        # ✅ Convert students from JSON string to a Python list
        if isinstance(data.get("students"), str):
            try:
                data["students"] = json.loads(data["students"])  # Convert JSON string to list
            except json.JSONDecodeError:
                return Response({"error": "Invalid students format"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ClassSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        try:
            # Parse students (ensure it's a list)
            students = request.data.get("students", [])
            if isinstance(students, str):
                students = json.loads(students)  # Convert JSON string to Python list

            instructor_id = request.data.get("instructor")
            course_id = request.data.get("course")

            print("Received students:", students)  # Debugging output

            valid_students = []
            for student_id in students:
                student = SignUp.objects.filter(id=student_id, role="student").first()
                if student:
                    lead = Leads.objects.filter(email=student.email, course_name=course_id).first()
                    if lead and lead.payment_status:
                        valid_students.append(student_id)
                    else:
                        return Response(
                            {"error": f"Student {student.username} has not completed payment."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                else:
                    return Response(
                        {"error": "Only students can be added to the class."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Validate instructor
            if instructor_id:
                instructor = SignUp.objects.filter(id=instructor_id, role="instructor").first()
                if not instructor:
                    return Response(
                        {"error": "Only instructors can be assigned to the class."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            return super().create(request, *args, **kwargs)

        except json.JSONDecodeError:
            return Response({"error": "Invalid students format"}, status=status.HTTP_400_BAD_REQUEST)





class ClassUpdateView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    lookup_field = 'pk'

class ClassDeleteView(generics.DestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Class.objects.all()
    lookup_field = 'pk'


class ClassListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

class InstructorListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        instructors = SignUp.objects.filter(role='instructor')  # Get only instructors
        serializer = SignUpSerializer(instructors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()  # ✅ Make a mutable copy of request data
        data['role'] = 'instructor'  # ✅ Set role to 'instructor' before saving

        serializer = SignUpSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class StudentListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        students = SignUp.objects.filter(role='student')  # Get only students
        serializer = SignUpSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
