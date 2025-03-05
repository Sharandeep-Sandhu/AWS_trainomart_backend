from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, BlogViewSet, LeadViewSet, ContactMessageViewSet, BusinessLeadsViewSet, BlogDetailView, CourseRegistrationView, sitemap_data, StudentPaymentStatusView, dashboard_data, get_csrf_token, LogoutView, UserListView, UpdateUserRoleView, student_profile, RetrieveUserView, RetrieveUpdateUserView, UpdateUserRoleView, EnrolledClassesView, ClassListView #, InstructorCreateView, InstructorListView, InstructorViewSet, StudentViewSet, ClassViewSet,SignUpView, LoginView
from . import views
from .views import (
    SignUpCreateView, SignUpUpdateView, SignUpDeleteView,
    ClassCreateView, ClassUpdateView, ClassDeleteView, InstructorListView,
    StudentListView
)


from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'blogs', BlogViewSet, basename='blog')
router.register(r'leads', LeadViewSet)
router.register(r'contact', ContactMessageViewSet)
router.register(r'quote', BusinessLeadsViewSet, basename='quote')
# router.register(r'instructors', InstructorViewSet, basename='instructor')
# router.register(r'students', StudentViewSet, basename='student')
# router.register(r'classes', ClassViewSet, basename='class')


urlpatterns = [
    path("", views.index, name="index"),
    path('api/', include(router.urls)),
    path('api/blogs/slug/<slug:slug>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('api/courses/<slug:slug>/', CourseViewSet.as_view({'get': 'get_course_by_slug'}), name='course-detail-by-slug'),
    path('api/register/', CourseRegistrationView.as_view(), name='course_registration'),
    path('api/sitemap/', views.sitemap_data, name='sitemap_data'), 
    # path('api/instructors/', InstructorListView.as_view(), name='instructor-list'),
    # path('api/instructors/create/', InstructorCreateView.as_view(), name='instructor-create'),
    path('api/student-payment-status/<str:email>/', StudentPaymentStatusView.as_view(), name='student-payment-status'),
    path("api/dashboard/", dashboard_data, name="dashboard-data"),
    path("api/csrf/", get_csrf_token, name="csrf_token"),
    path('api/students/profile/', student_profile, name='student-profile'),  # ✅ Route to get logged-in student
    # path("api/signup/", SignUpView.as_view(), name="signup"),
    # path("api/login/", LoginView.as_view(), name="login"),
    path("api/logout/", LogoutView.as_view(), name="logout"),
    path('api/instructors/', InstructorListView.as_view(), name='instructor-list'),
    path("api/users/", UserListView.as_view(), name="get_all_users"),  # ✅ Get all users
    path("api/users/<int:user_id>/update-role/", UpdateUserRoleView.as_view(), name="update_user_role"),  # ✅ Update user role
    path("api/users/<int:user_id>/", RetrieveUserView.as_view(), name="get-user-by-id"),
    path("api/users/<int:user_id>/update/", RetrieveUpdateUserView.as_view(), name="get-update-user-by-id"),
    path("api/users/<int:user_id>/role/", UpdateUserRoleView.as_view(), name="update-user-role"),
    path("api/users/<int:user_id>/enrolled-classes/", EnrolledClassesView.as_view(), name="enrolled-classes"),
    path('api/students/', StudentListView.as_view(), name='student-list'),

    
    
    path('signup/create/', SignUpCreateView.as_view(), name='signup-create'),
    path('signup/update/<int:pk>/', SignUpUpdateView.as_view(), name='signup-update'),
    path('signup/delete/<int:pk>/', SignUpDeleteView.as_view(), name='signup-delete'),

    path('api/class/', ClassListView.as_view(), name='class-create'),
    path('api/class/create/', ClassCreateView.as_view(), name='class-create'),
    path('api/class/update/<int:pk>/', ClassUpdateView.as_view(), name='class-update'),
    path('api/class/delete/<int:pk>/', ClassDeleteView.as_view(), name='class-delete'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
