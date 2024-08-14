from django.shortcuts import render,redirect
from decimal import Decimal
from NSQF import settings
from .models import *
from django.contrib.auth import login,logout,authenticate
from datetime import date
# Create your models here.
from django.db import models
# Create your models here.
import datetime

# Create your models here.
class TP(models.Model):
    Cat=models.CharField(max_length=100,default="X")
    Batch_Code = models.CharField(max_length=100,default='NA')
    Roll_No = models.CharField(max_length=100,default='NA')
    Course_Name = models.CharField(max_length=100,default='certified computer application accounting and publishing',null=True)
    Registration_number = models.IntegerField(null=True)
    Name_of_the_Candidate = models.CharField(max_length=100,default='NA')
    Mother_Name = models.CharField(max_length=100,default='NA')
    Father_Name = models.CharField(max_length=100,default='NA')
    DOB = models.DateField(null=True)
    Name_of_the_training_Partner = models.CharField(max_length=200,default='NA')
    Code_of_the_training_Partner = models.CharField(max_length=200,default='NA')
    Practical1 = models.CharField(max_length=100,default='NA')
    Practical2 = models.CharField(max_length=100,default='NA')
    IS1 = models.CharField(max_length= 100, null= True )
    IS2 = models.CharField(max_length= 100, null = True)
    Internal_Assessment = models.IntegerField(null=True)
    Project = models.CharField(max_length=100,default='NA')
    Major_Project = models.CharField(max_length=100, default='NA')
    Major_Project2 = models.CharField(max_length=100, default='NA')
    Typing_Speed=models.CharField(max_length=100, default='NA')
    Theory1=models.CharField(max_length=100, default='NA')
    Theory2=models.CharField(max_length=100, default='NA')
    # Total=models.CharField(max_length=100, default='NA')
    Center_code = models.CharField(max_length=100,  default='NA')
    Total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    Email_office = models.EmailField(null=True)
    Date_of_Exam = models.DateField(null=True)
    def __str__(self):
        return self.Course_Name
