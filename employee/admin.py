from django.contrib import admin
from .models import TP
from import_export.admin import ImportExportModelAdmin
# Register your models here.
# admin.site.register(TP,ImportExportModelAdmin)

class TPAdmin(ImportExportModelAdmin):
    # list_display=['id','Cat','Batch_Code','Roll_No']
    list_per_page = 50
    list_display=['id','Cat', 'Batch_Code', 'Roll_No', 'Course_Name', 'Registration_number', 'Center_code' , 'Name_of_the_Candidate','Practical1','IS1', 'IS2', 'Internal_Assessment', 'Project', 'Typing_Speed', 'Theory1', 'Theory2', 'Total','Date_of_Exam','Email_office']

admin.site.register(TP,TPAdmin)




