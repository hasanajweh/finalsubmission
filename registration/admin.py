from django.contrib import admin
from .models import CustomUser, Student, Course, CourseSchedule, StudentRegistration
from django.shortcuts import render
from .models import Notification
# Register CustomUser, Student, CourseSchedule, and StudentRegistration models as is.
admin.site.register(CustomUser)
admin.site.register(Student)
admin.site.register(CourseSchedule)
admin.site.register(StudentRegistration)

# Register Course model with additional configuration via CourseAdmin class.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'instructor')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['message', 'date_created', 'active', 'deadline_date']
    list_filter = ['active', 'date_created']
    search_fields = ['message']