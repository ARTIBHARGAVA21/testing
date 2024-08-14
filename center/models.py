from django.db import models
from faculty.models import*

# Create your models here.


class CourseSubmission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=255)
    submission_date = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.user.username} - {self.course_name} - {self.submission_date}"
