from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','first_name', 'last_name','username','email','role','is_superuser','is_staff']
    # search_fields = ('username', 'email', 'first_name', 'last_name')

admin.site.register(Class)
admin.site.register(Course)
admin.site.register(StudentClassEnrollment)
admin.site.register(Marks)