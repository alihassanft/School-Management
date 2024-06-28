from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)



class Class(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    classes = models.ManyToManyField(Class, related_name='courses')
    teachers = models.ManyToManyField(User, limit_choices_to={'role': 'teacher'}, related_name='courses')

    def __str__(self):
        return self.name

class StudentClassEnrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, related_name='enrollments')
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='enrollments')

    def __str__(self):
        return f"{self.student.username} - {self.class_obj.name}"

class Marks(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, related_name='marks')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='marks')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'}, related_name='given_marks')
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='marks')
    mark = models.FloatField()

    def __str__(self):
        return f"{self.student.username} - {self.course.name} - {self.mark}"




