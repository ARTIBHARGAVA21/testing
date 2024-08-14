from django.contrib import admin

# Register your models here.
from .models import CourseSubmission
class CourseSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'course_name', 'submission_date')
    list_filter = ('user', 'course_name', 'submission_date')
    search_fields = ('user__username', 'course_name')
    ordering = ('-submission_date',)

admin.site.register(CourseSubmission, CourseSubmissionAdmin)
