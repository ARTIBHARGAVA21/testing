from django.contrib import admin
from django.urls import path,include
from employee.views import *
from faculty.views import *
from center.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('data/', save_data, name='save_data'),
    path('download_report/',download_report,name='download_report'),
    path('download_report_data/',download_report_data,name='download_report_data'),
    path('',index),
    path('logout/',Logout),
    path('admin_login',admin_login,name='admin_login'),
    path('admin_home',admin_home,name='admin_home'),
    path('change_passwordadmin',change_passwordadmin,name='change_passwordadmin'),
    path('all_employee',all_employee, name='all_employee'),
    path('all_employee_data',all_employee_data, name='all_employee_data'),
    path('display_data/',display_data,name='display_data'),
    path('display_data_data/',display_data_data,name='display_data_data'),
    path('nielitheader/',nielitheader,name='nielitheader'),
    path('faculty_signup_data/',create_non_staff_user,name='faculty_signup_data'),
    path('faculty_home/',faculty_home,name='faculty_home'),
    path('attandance/', attandancedetail, name= 'attandancedetail' ),
    path('attandance_center/', attandancedetail_center, name='attandancedetail_center'),
    path('internal_marks/', internal_ass, name = 'internal_ass'),
    path('faculty_save/', faculty_save_data, name ='faculty_save_data'),
     path('admin-view-course/<str:course_name>/', view_course, name='admin_view_course'),
    path('faculty_save_practical/', faculty_save_practical_data, name='faculty_save_practical_data'),
    path('faculty_save_assignment/', faculty_save_assignment_data, name='faculty_save_practical_data'),
    path('logout_faculty/', Logout_faculty, name='logout_faculty'),
    path('center_download/', center_download, name = 'center_download'  ),
    path('center_month/', internal_center_marks, name = 'center_month' ),
    path('center_home/', center_home, name='center_home' ),
    path('faculty_signup_data_center/', create_non_staff_user_center, name='faculty_signup_data_center' )
    ]
