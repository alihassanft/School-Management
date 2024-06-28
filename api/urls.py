from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'class', ClassViewSet)
router.register(r'course', CourseViewSet)
router.register(r'marks', MarksViewSet)

urlpatterns = [
    # user
    path('login/',UserLoginAPIView.as_view(),name='login'),
    path('signup/',UserSignUpAPIView.as_view(),name='signup'),
    path('get_user/',GetUserDetailsAPIView.as_view(),name='get-user'),
    path('get_all_users/',GetAllUsersAPIView.as_view(),name='users'),
    path('enrollments/', EnrollmentListCreateAPIView.as_view(), name='enrollment-list-create'),
    path('students_courses_for_specfic_class/', StudentCoursesAPIView.as_view(), name='student-courses'),
    path('student-marks/', StudentMarksAPIView.as_view(), name='student-marks'),
    path('', include(router.urls)),
]
