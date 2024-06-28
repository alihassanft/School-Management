from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import *
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny,IsAuthenticated
from .permissions import *
from .pagination import *
from .filters import *
# Create your views here.

#customer tokenobrainpiar view to get user information 
class UserLoginAPIView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        required_fields = ['username', 'password']
        missing_fields = [field for field in required_fields if field not in request.data]
        if missing_fields:
            errors = {field:["This field is required."] for field in missing_fields }
            return Response(errors,status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        token = serializer.validated_data.get('access')
        refresh = serializer.validated_data.get('refresh')
        data = {
            'access_token': token,
            'refresh_token': refresh,
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'role':user.role,
            }}
        return Response({"data":data}, status=status.HTTP_200_OK)

# signup
class UserSignUpAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# fetch and update user/teacher/student 
class GetUserDetailsAPIView(APIView):
    def get(self,request):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def patch(self, request):
        user = self.request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Get All Teachers only superuser can access this api
class GetAllUsersAPIView(APIView):
    def get(self,request):
        user = self.request.user
        if user.is_superuser == True:
            role = request.query_params.get('role')
            if role:
                user_data = User.objects.filter(role=role)
            else:
                user_data = User.objects.all()
            search_fields = ['first_name', 'last_name', 'username', 'email']
            for field in search_fields:
                search_value = request.query_params.get(field, None)
                if search_value:
                    user_data = user_data.filter(**{f"{field}__icontains": search_value})
            paginator = CustomPagination()
            paginated_user_data = paginator.paginate_queryset(user_data, request)
            user_serializer = UserSerializer(paginated_user_data,many=True)
            # return Response({"data":user_serializer.data})
            return paginator.get_paginated_response(user_serializer.data)
        else:
            return Response({"detail":"Only SuperUser can access this api"})

# classes
class ClassViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,IsTeacher]
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    pagination_class = CustomPagination  #pagination
    filter_backends = [CustomSearchFilter]  # Add custom search filter backend
    search_fields = ['name']  # Specify fields to search against

# course
class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,IsTeacher]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination   #pagination
    filter_backends = [CustomSearchFilter]  # Add custom search filter backend
    search_fields = ['name']  # Specify fields to search against

# enroll student against class
class EnrollmentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated,IsTeacher]
    def get(self, request):
        enrollments = StudentClassEnrollment.objects.all()
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# marks only acces by teacher
class MarksViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,IsTeacher]
    queryset = Marks.objects.all()
    serializer_class = MarksSerializer

# Retrieving a student's enrolled courses for a specific class.
class StudentCoursesAPIView(APIView):
    def get(self, request):
        try:
            user = self.request.user
            if user.role == "student":
                # Filter enrollments for the specific student
                enrollments = StudentClassEnrollment.objects.filter(student=user.id)
                response_data = []
                for enrollement in enrollments:
                    class_obj = enrollement.class_obj
                    courses = Course.objects.filter(classes = class_obj).distinct()
                    courses_names = [course.name for course in courses]
                    response_data.append({
                        "student_id":user.id,
                        "student_name":user.first_name,
                        "class name":class_obj.name,
                        "courses":courses_names
                    })

                return Response({"data":response_data})
            else:
                return Response({'resp':"student only access this api"})
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class StudentMarksAPIView(APIView):
    def get(self, request):
        user = self.request.user
        if user.role == "student":
            class_id = request.query_params.get('class_id')
            course_id = request.query_params.get('course_id')
            if class_id and course_id:
                try:
                    marks = Marks.objects.filter(student_id=user.id, class_obj_id=class_id, course_id=course_id)
                    serializer = MarksSerializer(marks, many=True)
                    return Response(serializer.data)
                except Marks.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"resp":"student only access this api"})













