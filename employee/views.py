  # P1 Files
from django.forms import IntegerField
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .models import TP
from django.core.mail import send_mail
from django.core import mail
from django.core.mail.message import EmailMessage
from faculty.models import *
from django.db.models.functions import Cast
# P2 NSQF File
from django.shortcuts import render
from .models import *
from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.http import JsonResponse
# from .forms import DataReqUpdateForm
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'index.html')


def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('admin_home')
            elif user is not None and user.center_code:
                login(request, user)
                return redirect('center_home')
            elif user is not None:
                login(request, user)
                # user = request.user
                # record = Faculty.objects.get(user=user)
                # coursename = record.coursename
                # data = TP.objects.filter(Course_Name__icontains=coursename)
                return redirect('/internal_marks/')
            else:
                messages.error(request, "Invalid credentials. Please try again.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    return render(request, 'admin_login.html')

# def admin_login(request):
#     error = ""
#     if request.method == 'POST':
#         u = request.POST['username']
#         p = request.POST['pwd']
#         user = authenticate(username=u, password=p)
#         try:
#             if user.is_staff:
#                 login(request, user)
#                 return redirect('admin_home')
#             elif request.user:
#                 login(request, user)

#                 # user=request.user
#                 # record=Faculty.objects.get(user=user)
#                 # coursename=record.coursename
#                 # data=TP.objects.filter(Course_Name__icontains=coursename)
#                 return redirect('faculty_home')
#             else:
#                 print("Hello user 3")
#                 error = "yes"
#         except:
#             error = "yes"
#     else:
#         return render(request, 'admin_login.html')

def view_course(request, course_name):
    candidates = TP.objects.filter(Course_Name__icontains=course_name)
    context = {
        'course_name': course_name,
        'candidates': candidates
    }
    return render(request, 'course_detail.html', context)


def faculty_home(request):
    if not request.user:
        return redirect('admin_login')
    user=request.user
    record = CustomUser.objects.get(username=user)
    coursename=record.course_name
    data=TP.objects.filter(Course_Name__icontains=coursename)
    return render(request,'faculty_home.html',locals())

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    total=TP.objects.all()
    total_exam=total.count()
    # CMD Result
    total_cmd=total.filter(Course_Name__icontains='Multimedia').count()
    # Practical 01
    total_cmd_p1_ab=total.filter(Q(Course_Name__icontains="Multimedia",Practical1__icontains = 'ab')).count()
    total_cmd_p1_fail=total.filter(Q(Course_Name__icontains = "Multimedia",Practical1__lt='30',Practical1__gte='0.0')).count()
    total_cmd_p1_pass=total.filter(Q(Course_Name__icontains = "Multimedia",Practical1__gte='30',Practical1__lte='60')).count()

     # Theory 01 - CMD
    total_cmd_t1_ab=total.filter(Q(Course_Name__icontains="Multimedia",Theory1__icontains = 'ab')).count()
    total_cmd_t1_fail=total.filter(Q(Course_Name__icontains = "Multimedia",Theory1__lt='50',Theory1__gte='0.0')).count()
    total_cmd_t1_pass=total.filter(Q(Course_Name__icontains = "Multimedia",Theory1__gte='50',Theory1__lte='99.99')).count()
    

    # Overall  - CMD
    total_cmd_over_ab=total.filter(Q(Course_Name__icontains="Multimedia",Practical1__icontains = 'ab')|Q(Course_Name__icontains="Multimedia",Theory1__icontains = 'ab')).count()

    
    total_cmd_over_pass=total.filter(Q(Course_Name__icontains = "Multimedia",Theory1__lte='99.99',Theory1__gte='50.0') & Q(Course_Name__icontains = "Multimedia",Practical1__lte='60.00',Practical1__gte='30.0')).count()
    total_cmd_over_fail=total_cmd-total_cmd_over_pass-total_cmd_over_ab

   
    ##  CWD
    total_cwd=total.filter(Course_Name__icontains ='Web Developer').count()

    total_cwd_p1_ab=total.filter(Q(Course_Name__icontains="web developer",Practical1__icontains = 'ab')).count()
    total_cwd_p1_fail=total.filter(Q(Course_Name__icontains = "web developer",Practical1__lt='45',Practical1__gte='0.0')).count()
    total_cwd_p1_pass=total.filter(Q(Course_Name__icontains = "web developer",Practical1__gte='45',Practical1__lte='90')).count()

     # Theory 01 - CWD
    total_cwd_t1_ab=total.filter(Q(Course_Name__icontains="web developer",Theory1__icontains = 'ab')).count()
    total_cwd_t1_fail=total.filter(Q(Course_Name__icontains = "web developer",Theory1__lt='50',Theory1__gte='0.0')).count()
    total_cwd_t1_pass=total.filter(Q(Course_Name__icontains = "web developer",Theory1__gte='50',Theory1__lte='99.99')).count()
    
     # Theory 02 - CWD

    total_cwd_t2_ab=total.filter(Q(Course_Name__icontains="web developer",Theory2__icontains = 'ab')).count()
    total_cwd_t2_fail=total.filter(Q(Course_Name__icontains = "web developer",Theory2__lt='50',Theory2__gte='0.0')).count()
    total_cwd_t2_pass=total.filter(Q(Course_Name__icontains = "web developer",Theory2__gte='50',Theory2__lte='99.99')).count()
    
    # Overall  - CWD
    total_cwd_over_ab=total.filter(Q(Course_Name__icontains="web developer",Practical1__icontains = 'ab')|Q(Course_Name__icontains="web developer",Theory1__icontains = 'ab')|Q(Course_Name__icontains="web developer",Theory2__icontains = 'ab')).count()
    
    total_cwd_over_pass=total.filter(Q(Course_Name__icontains = "web developer",Theory2__lte='99.99',Theory2__gte='50.0') & Q(Course_Name__icontains = "web developer",Theory1__lte='99.99',Theory1__gte='50.0') & Q(Course_Name__icontains = "web developer",Practical1__lte='90.00',Practical1__gte='45.0')).count()
    total_cwd_over_fail=total_cwd-total_cwd_over_pass-total_cwd_over_ab
    ## CAAPA
    total_caapa=total.filter(Course_Name__icontains ='accounting').count()
    total_caapa_p1_ab=total.filter(Q(Course_Name__icontains="accounting",Practical1__icontains = 'ab')).count()
    total_caapa_p1_fail=total.filter(Q(Course_Name__icontains = "accounting",Practical1__lt='45.00',Practical1__gte='0.0')).count()
    total_caapa_p1_pass=total.filter(Q(Course_Name__icontains = "accounting",Practical1__gte='45.00',Practical1__lte='90.00')).count()

     # Theory 01 - CAAPA
    total_caapa_t1_ab=total.filter(Q(Course_Name__icontains="accounting",Theory1__icontains = 'ab')).count()
    total_caapa_t1_fail=total.filter(Q(Course_Name__icontains = "accounting",Theory1__lt='50',Theory1__gte='0.0')).count()
    total_caapa_t1_pass=total.filter(Q(Course_Name__icontains = "accounting",Theory1__gte='50',Theory1__lte='99.99')).count()
    

     # Theory 02 - CAAPA
    total_caapa_t2_ab=total.filter(Q(Course_Name__icontains="accounting",Theory2__icontains = 'ab')|Q(Course_Name__icontains="accounting",Theory2__icontains = 'na')).count()
    total_caapa_t2_fail=total.filter(Q(Course_Name__icontains = "accounting",Theory2__lt='50',Theory2__gte='0.0')).count()
    total_caapa_t2_pass=total.filter(Q(Course_Name__icontains = "accounting",Theory2__gte='50',Theory2__lte='99.99')).count()

    # Overall  - CAAPA
    total_caapa_over_ab=total.filter(Q(Course_Name__icontains="accounting",Practical1__icontains = 'ab')|Q(Course_Name__icontains="accounting",Theory1__icontains = 'ab')|Q(Course_Name__icontains="accounting",Theory2__icontains = 'ab')|Q(Course_Name__icontains="accounting",Theory2__icontains = 'na')).count()

    total_caapa_over_pass=total.filter(Q(Course_Name__icontains = "accounting",Theory2__lte='99.99',Theory2__gte='50.0') & Q(Course_Name__icontains = "accounting",Theory1__lte='99.99',Theory1__gte='50.0') & Q(Course_Name__icontains = "accounting",Practical1__lte='90.00',Practical1__gte='45.0')).count()

    total_caapa_over_fail=total_caapa-total_caapa_over_pass-total_caapa_over_ab

    # Data Entry & Office Automation
    total_deo=total.filter(Course_Name__icontains='Data Entry').count()
    # Practical 01
    total_deo_p1_ab=total.filter(Q(Course_Name__icontains="Data Entry",Practical1__icontains = 'ab')).count()
    total_deo_p1_fail=total.filter(Q(Course_Name__icontains = "Data Entry",Practical1__lt='30',Practical1__gte='0.0')).count()
    total_deo_p1_pass=total.filter(Q(Course_Name__icontains = "Data Entry",Practical1__gte='30.00',Practical1__lte='60.00')).count()

    # Typing Speed
    total_deo_tp_ab=total.filter(Q(Course_Name__icontains="Data Entry",Typing_Speed__icontains = 'ab')).count()
    total_deo_tp_fail=total.filter(Q(Course_Name__icontains = "Data Entry",Typing_Speed__lt='35.00',Typing_Speed__gte='0.0')).count()
    total_deo_tp_pass=total.filter(Q(Course_Name__icontains = "Data Entry",Typing_Speed__gte='35.00',Typing_Speed__lte='99.00')).count()

     # Theory 01 - DEO
    total_deo_t1_ab=total.filter(Q(Course_Name__icontains="Data Entry",Theory1__icontains = 'ab')).count()
    total_deo_t1_fail=total.filter(Q(Course_Name__icontains = "Data Entry",Theory1__lt='50',Theory1__gte='0.0')).count()
    total_deo_t1_pass=total.filter(Q(Course_Name__icontains = "Data Entry",Theory1__gte='50',Theory1__lte='99.99')).count()

    # Overall  - DEO
    total_deo_over_ab=total.filter(Q(Course_Name__icontains="Data Entry",Practical1__icontains = 'ab')|Q(Course_Name__icontains="Data Entry",Theory1__icontains = 'ab')).count()

    total_deo_over_pass=total.filter(Q(Course_Name__icontains = "data entry",Theory1__lte='99.99',Theory1__gte='50.0') & Q(Course_Name__icontains = "data entry",Practical1__lte='60',Practical1__gte='30')).count()
    total_deo_over_fail=total_deo-total_deo_over_pass-total_deo_over_ab

    ##
    # Cyber Security
    total_csa=total.filter(Course_Name__icontains='Cyber Security').count()
    # Practical
    total_csa_p1_ab=total.filter(Q(Course_Name__icontains="cyber security",Practical1__icontains = 'ab')).count()
    total_csa_p1_fail=total.filter(Q(Course_Name__icontains = "cyber security",Practical1__lt='45',Practical1__gte='0.0')).count()
    total_csa_p1_pass=total.filter(Q(Course_Name__icontains = "cyber security",Practical1__gte='45',Practical1__lte='90')).count()
   
    print("Total Course :", total_exam,total_cmd,total_cwd,total_caapa,total_deo,total_csa)
     # Theory 01 - CSA
    total_csa_t1_ab=total.filter(Q(Course_Name__icontains="cyber security",Theory1__icontains = 'ab')).count()
    total_csa_t1_fail=total.filter(Q(Course_Name__icontains = "cyber security",Theory1__lt='50',Theory1__gte='0.0')).count()
    total_csa_t1_pass=total.filter(Q(Course_Name__icontains = "cyber security",Theory1__gte='50',Theory1__lte='99.99')).count()
    
     # Theory 02 - CSA
    total_csa_t2_ab=total.filter(Q(Course_Name__icontains="cyber security",Theory2__icontains = 'ab')).count()
    total_csa_t2_fail=total.filter(Q(Course_Name__icontains = "cyber security",Theory2__lt='50',Theory2__gte='0.0')).count()
    total_csa_t2_pass=total.filter(Q(Course_Name__icontains = "cyber security",Theory2__gte='50',Theory2__lte='99.99')).count()
    
    # Overall  - CSA
    total_csa_over_ab=total.filter(Q(Course_Name__icontains="cyber security",Practical1__icontains = 'ab')|Q(Course_Name__icontains="cyber security",Theory1__icontains = 'ab')|Q(Course_Name__icontains="cyber security",Theory2__icontains = 'ab')).count()

    total_csa_over_pass=total.filter(Q(Course_Name__icontains = "cyber security",Theory2__lte='99.99',Theory2__gte='50.0') & Q(Course_Name__icontains = "cyber security",Theory1__lte='99.99',Theory1__gte='50.0') & Q(Course_Name__icontains = "cyber security",Practical1__lte='90.00',Practical1__gte='45.0')).count()
    total_csa_over_fail=total_csa-total_csa_over_pass-total_csa_over_ab

    # Total pass
    total_over_pass= total_cmd_over_pass + total_caapa_over_pass + total_csa_over_pass+ total_cwd_over_pass+total_deo_over_pass
    total_over_fail= total_cmd_over_fail + total_caapa_over_fail + total_csa_over_fail+ total_cwd_over_fail+total_deo_over_fail
    total_over_ab= total_cmd_over_ab + total_caapa_over_ab + total_csa_over_ab+ total_cwd_over_ab+total_deo_over_ab
    total_over=total_over_pass+total_over_fail+total_over_ab
    total_over_pass_per=(total_over_pass/total_over)*100
    total_over_pass_per=round(total_over_pass_per,1)
    total_over_fail_per=(total_over_fail/total_over)*100
    total_over_fail_per=round(total_over_fail_per,1)
    total_over_ab_per=(total_over_ab/total_over)*100
    total_over_ab_per=round(total_over_ab_per,1)
    return render(request, 'admin_home.html',locals())
def all_employee_data(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    user=request.user
    record=CustomUser.objects.get(username=user)
    coursename=record.course_name
    data=TP.objects.filter(Course_Name__icontains=coursename)
    return render(request, 'all_employee_data.html',locals())

def all_employee(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    employee = TP.objects.all()
    return render(request, 'all_employee.html',locals())
def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method=="POST":
        o = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"
    return render(request,'change_passwordadmin.html',locals())
def Logout(request):
    logout(request)
    return redirect('/')


def download_report_data(request):
    user=request.user
    record=CustomUser.objects.get(username=user)
    coursename=record.course_name
    data=TP.objects.filter(Course_Name__icontains=coursename)
    # print("Hello Record",data)
    if request.method == 'POST':
        f = request.POST.get('fromdate')
        t = request.POST.get('todate')
        bc = request.POST.get('batch_code')
        cn = request.POST.get('course_name')
        print("Hello JI",f,t,bc,cn)
        # if f and t:
        #     try:
        #         from_date_parsed = datetime.strptime(f, '%Y-%m-%d').date()
        #         to_date_parsed = datetime.strptime(t, '%Y-%m-%d').date()
        #         print('New',from_date_parsed,to_date_parsed)
        #     except ValueError:
        #         from_date_parsed = None
        #         to_date_parsed = None
        # else:
        #     from_date_parsed = None
        #     to_date_parsed = None
    # Filter the data based on the provided criteria
        data=TP.objects.filter(Course_Name__icontains=coursename)
        # if from_date_parsed and to_date_parsed:
        #     data = data.filter(Date_of_Exam__range=(from_date_parsed, to_date_parsed))
        if f and t:
            data=data.filter(Date_of_Exam__range=(f,t))
        if bc:
            data = data.filter(Batch_Code__iexact=bc)
        if cn:
            data = data.filter(Course_Name__iexact=cn)


    course_names = TP.objects.values_list('Course_Name', flat=True).distinct()
    batch_codes = TP.objects.values_list('Batch_Code', flat=True).distinct()

    # Prepare context for rendering template
    context = {'data': data,
               'course_names': course_names,
               'batch_codes': batch_codes,}

    return render(request, 'download_report_data.html', context)

# def download_report(request):
#     data=TP.objects.all()
#     cn = None
#     bc = None
#     # print("Hello Record",data)
#     if request.method == 'POST':
#         f = request.POST.get('fromdate')
#         t = request.POST.get('todate')
#         bc = request.POST.get('batch_code')
#         cn = request.POST.get('course_name')
#         data = TP.objects.all()
#         if f and t:
#             data=data.filter(Date_of_Exam__range=(f,t))
#         if bc:
#             data = data.filter(Batch_Code__iexact=bc)
#         if cn:
#             data = data.filter(Course_Name__iexact=cn)


#     course_names = TP.objects.values_list('Course_Name', flat=True).distinct()
#     batch_codes = TP.objects.values_list('Batch_Code', flat=True).distinct()

#     # Prepare context for rendering template
#     context = {'data': data,
#                 'cn':cn,
#                 'bc':bc,
#                'course_names': course_names,
#                'batch_codes': batch_codes,}


#     return render(request, 'download_report.html', context)

EXCLUDED_EMAIL = 'example@example.com'

@login_required
def download_report(request):
    data = TP.objects.all()
    cn = None
    bc = None

    if request.method == 'POST':
        f = request.POST.get('fromdate')
        t = request.POST.get('todate')
        bc = request.POST.get('batch_code')
        cn = request.POST.get('course_name')
        data = TP.objects.all()
        if f and t:
            data = data.filter(Date_of_Exam__range=(f, t))
        if bc:
            data = data.filter(Batch_Code__iexact=bc)
        if cn:
            data = data.filter(Course_Name__iexact=cn)

        send_all = request.POST.get('send_all')
        employee_id = request.POST.get('employee_id')

        if send_all:
            employees = TP.objects.all()
        elif employee_id:
            try:
                employees = [TP.objects.get(id=employee_id)]
            except TP.DoesNotExist:
                employees = []
                print(f"Student with id {employee_id} does not exist.")
        else:
            employees = []

        for student in employees:
            if student.Email_office and student.Email_office != EXCLUDED_EMAIL:
                practical1 = student.Practical1
                practical2 = student.Practical2
                is1 = student.IS1
                is2 = student.IS2
                internal_assessment = student.Internal_Assessment
                project = student.Project
                major_project = student.Major_Project
                major_project2 = student.Major_Project2
                typing_speed = student.Typing_Speed
                theory1 = student.Theory1
                theory2 = student.Theory2
                total = student.Total

                detailed_message = f'''
                Dear {student.Name_of_the_Candidate},

                Here are your subject scores:
                - Practical 1: {practical1}
                - Practical 2: {practical2}
                - IS1: {is1}
                - IS2: {is2}
                - Internal Assessment: {internal_assessment}
                - Project: {project}
                - Major Project: {major_project}
                - Major Project 2: {major_project2}
                - Typing Speed: {typing_speed}
                - Theory 1: {theory1}
                - Theory 2: {theory2}
                - Total: {total}

                Your overall status is: {'Pass' if float(total) > 30 else 'Fail'}.

                Best regards,
                Your Training Team
                '''

                subject = f'Result Notification for {student.Name_of_the_Candidate}'
                from_email = settings.EMAIL_HOST_USER

                try:
                    send_mail(subject, detailed_message, from_email, [student.Email_office])
                    print(f"Email sent to student {student.Name_of_the_Candidate} ({student.Email_office}) successfully.")
                except Exception as e:
                    print(f"Failed to send email to student {student.Name_of_the_Candidate} ({student.Email_office}): {str(e)}")
            else:
                print(f"Student {student.Name_of_the_Candidate} does not have a valid email address.")

    course_names = TP.objects.values_list('Course_Name', flat=True).distinct()
    batch_codes = TP.objects.values_list('Batch_Code', flat=True).distinct()

    context = {
        'data': data,
        'cn': cn,
        'bc': bc,
        'course_names': course_names,
        'batch_codes': batch_codes,
    }

    return render(request, 'download_report.html', context)

# P2 View NSQF
def all_employee(request):
    data = TP.objects.all()
    context = {'data': data}
    return render(request, 'all_employee.html', context)
def save_data(request):
    if request.method == 'POST':
        field1 = request.POST.get('practical1')
        field2 = request.POST.get('internal')
        field3 = request.POST.get('project')
        field4 = request.POST.get('typing_speed')
        field5 = request.POST.get('theory1')
        field6 = request.POST.get('theory2')
        field7 = request.POST.get('total')
        obj_id = request.POST.get('id')
        try:
            obj = TP.objects.get(pk=obj_id)
            obj.Practical1 = field1
            obj.Internal_Assessment = field2
            obj.Project = field3
            obj.Typing_Speed = field4
            obj.Theory1 = field5
            obj.Theory2 = field6
            obj.Total = field7
            obj.save()
            return JsonResponse({'success': True})
        except TP.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Object not found'})
        except Exception as e:
            print("Error occurred while saving data:", e)
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

def display_data(request):
    query = request.POST.get('q')
    data=TP.objects.all()
    if query:
        filters = (
            Q(Roll_No__icontains=query) |
            Q(Registration_number__icontains=query) |
            Q(Name_of_the_Candidate__icontains=query) |
            Q(Mother_Name__icontains=query) |
            Q(Father_Name__icontains=query) |
            Q(DOB__icontains=query) |
            Q(Batch_Code__icontains=query)
        )
        data = data.filter(filters)
    context = {'data': data}
    return render(request, 'all_employee.html', context)

def display_data_data(request):
    query = request.POST.get('q')
    user=request.user
    record=Faculty.objects.get(user=user)
    coursename=record.coursename
    data=TP.objects.filter(Course_Name__icontains=coursename)
    if query:
        filters = (
            Q(Roll_No__icontains=query) |
            Q(Registration_number__icontains=query) |
            Q(Name_of_the_Candidate__icontains=query) |
            Q(Mother_Name__icontains=query) |
            Q(Father_Name__icontains=query) |
            Q(DOB__icontains=query) |
            Q(Batch_Code__icontains=query)
        )
        data = data.filter(filters)
    context = {'data': data}
    return render(request, 'all_employee_data.html', context)

def nielitheader(request):
    return render(request,"nielit_header2.html")

