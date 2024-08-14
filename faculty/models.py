from django.db import models
from faculty.models import *
from employee.models import *
# from django.contrib.auth.models import User

# Create your models here.

# class Faculty(models.Model):
#     #username=models.CharField(max_length=100,null=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
#     coursename = models.CharField(max_length=100,null=True,blank=True)
#     centername = models.CharField(max_length=100,null=True,blank=True)

# def faculty_login(request):
#     error = ""
#     if request.method == 'POST':
#         u = request.POST['username']
#         p = request.POST['pwd']
#         faculty=Faculty.objects.filter(user_username=u)
#         print(faculty.coursecode)
#         coursecode=faculty.coursecode
#         user = authenticate(username=u, password=p)
#         try:
#             if user:
#                 login(request, user)
#                 return redirect('faculty_home',{'coursecode':coursecode})
#             else:
#                 error = "yes"
#         except:
#             error = "yes"
#     return render(request, 'faculty_home',locals())

from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
import datetime


class CustomUser(AbstractUser):
    # Faculty-specific fields
    course_name = models.CharField(max_length=200, blank=True, null=True)
    center_name = models.CharField(max_length=100, blank=True, null=True)
    user_date = models.DateField(null=True)
    submission_date_practical = models.DateField(null=True)
    submitted_practical = models.BooleanField(default=False)
    submission_date_internal = models.DateField(null=True)
    submitted_internal = models.BooleanField(default=False)
    submission_date_assignment = models.DateField(null=True)
    submitted_assignment = models.BooleanField(default=False)
    center_code = models.CharField(null=True, max_length = 100)
    center_submitted = models.BooleanField(default=False)
    submission_date_center = models.DateField(null=True)
    faulty_login_attempts = models.IntegerField(default=0)

    # Add any additional customizations or methods as needed

    def __str__(self):
        return self.username  # Or any other field that represents the user
