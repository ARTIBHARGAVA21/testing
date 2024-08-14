from django.shortcuts import render
from faculty.models import *
from employee.models import *
from datetime import datetime
from django.contrib import messages
from .forms import SimpleUserCreationForm
from django.db.models import Q
from .models import CourseSubmission
# Create your views here.

def center_download(request):
    current_month = request.user.user_date.month
    current_year = request.user.user_date.year
    center = request.user.center_code
    # current_month = datetime.now().month
    # current_year = datetime.now().year

    # Calculate the start and end date of the current month
    start_date = datetime(current_year, current_month, 1)
    end_date = datetime(current_year, current_month + 1, 1) if current_month < 12 else datetime(current_year + 1, 1, 1)

    # Filter the data from TP model based on the current month and year
    student_display = TP.objects.filter(Date_of_Exam__gte=start_date, Date_of_Exam__lt=end_date).order_by('Name_of_the_Candidate')
    students = TP.objects.filter(Date_of_Exam__gte=start_date, Date_of_Exam__lt=end_date).order_by('Name_of_the_Candidate')
    students = students.filter(Center_code = center)


    context = {'data':students}
    return render(request, 'home.html', context)


def internal_center_marks(request):
    current_month = request.user.user_date.month
    current_year = request.user.user_date.year
    center = request.user.center_code

    # Check for date consistency
    try:
        start_date = datetime(current_year, current_month, 1)
        end_date = datetime(current_year, current_month + 1, 1) if current_month < 12 else datetime(current_year + 1, 1, 1)
    except Exception as e:
        messages.error(request, 'Date error')
        return render(request, 'error.html', {'message': 'Date error'})

    this_center = request.user.center_code
    data = TP.objects.filter(Date_of_Exam__gte=start_date, Date_of_Exam__lt=end_date).order_by('Name_of_the_Candidate')
    items = data.filter(Center_code=this_center)

    selected = request.GET.get('course_name')
    course_names = items.values_list('Course_Name', flat=True).order_by('Course_Name').distinct()

    if selected:
        items = items.filter(Course_Name__icontains=selected)

    user = request.user

    course_submission_exists = CourseSubmission.objects.filter(user=user, course_name=selected).exists()

    if request.method == 'POST':
        if course_submission_exists:
            messages.error(request, 'Internal assessment already submitted for this course')
            return redirect('/center_month/')

        for item in items:
            item_id = str(item.id)
            assignment = request.POST.get(f'assignment_{item_id}', '0')
            practical = request.POST.get(f'practical_{item_id}', '0')
            internal1 = request.POST.get(f'internal1_{item_id}', '0')
            internal2 = request.POST.get(f'internal2_{item_id}', '0')
            total_internal = request.POST.get(f'total_internal_{item_id}', '0')

            item.Project = assignment
            item.Practical1 = practical
            item.IS1 = internal1
            item.IS2 = internal2
            item.Internal_Assessment = total_internal
            item.save()

        CourseSubmission.objects.create(user=user, course_name=selected, submission_date=user.user_date)

        messages.success(request, 'Data successfully submitted')
        return redirect('/center_month/')

    return render(request, 'month_data.html', {
        'data': items,
        'course_names': course_names,
        'center_code': center,
        'selected_course': selected,
        'course_submission_exists': course_submission_exists,
        'user': user
    })





def attandancedetail_center(request):
    # Get the current month and year
    course = request.GET.get('course_name')
    current_month = request.user.user_date.month
    current_year = request.user.user_date.year
    center = request.user.center_code
    # current_month = datetime.now().month
    # current_year = datetime.now().year

    # Calculate the start and end date of the current month
    start_date = datetime(current_year, current_month, 1)
    end_date = datetime(current_year, current_month + 1, 1) if current_month < 12 else datetime(current_year + 1, 1, 1)

    # Filter the data from TP model based on the current month and year
    student_display = TP.objects.filter(Date_of_Exam__gte=start_date, Date_of_Exam__lt=end_date).order_by('Name_of_the_Candidate')
    students = TP.objects.filter(Date_of_Exam__gte=start_date, Date_of_Exam__lt=end_date).order_by('Name_of_the_Candidate')
    print(course)
    students = students.filter(Center_code= request.user.center_code)
    if course:
        student_display = students.filter(Course_Name__icontains=course)

    # Use distinct on the original field with order_by
    course_names = students.values_list('Course_Name', flat=True).order_by('Course_Name').distinct()

    print(f"Number of students after course filter: {students.count()}")
    context = {
        'course': course,
        'course_names': course_names,
        'students': student_display,
        'current_month': current_month,
        'current_year': current_year,
        'center_code': center,
    }
    return render(request, 'attandance_center.html', context)



def create_non_staff_user_center(request):
    if request.method == 'POST':
        form = SimpleUserCreationForm(request.POST)
        if form.is_valid():
            custom_user = form.save(commit=False)
            custom_user.is_staff = False
            custom_user.save()
            messages.success(request, 'Non-staff user created successfully!')
            # messages.success("Account Created successfully")
            return redirect('/faculty_signup_data/')
        else:
            messages.error(request, 'Something went wrong. Please correct the errors below.')
    else:
        form = SimpleUserCreationForm()
    return render(request, 'faculty_sign_up_center.html', {'form': form})





def center_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    total=TP.objects.all()
    center = request.user.center_code
    total = total.filter(Center_code = center)
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
    # total_course=TP.objects.filter('Course_Name')

    # Overall  - CMD
    total_cmd_over_ab=total.filter(Q(Course_Name__icontains="Multimedia",Practical1__icontains = 'ab')|Q(Course_Name__icontains="Multimedia",Theory1__icontains = 'ab')).count()

    # total_csa_over_fail=total.filter(Q(Course_Name__icontains = "cyber security",Theory2__lt='50',Theory2__gte='0.0')|Q(Course_Name__icontains = "cyber security",Theory1__lt='50',Theory1__gte='0.0')|Q(Course_Name__icontains = "cyber security",Practical1__lt='45',Practical1__gte='0.0')).count()

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
    # total_course=TP.objects.filter('Course_Name')

     # Theory 02 - CWD

    total_cwd_t2_ab=total.filter(Q(Course_Name__icontains="web developer",Theory2__icontains = 'ab')).count()
    total_cwd_t2_fail=total.filter(Q(Course_Name__icontains = "web developer",Theory2__lt='50',Theory2__gte='0.0')).count()
    total_cwd_t2_pass=total.filter(Q(Course_Name__icontains = "web developer",Theory2__gte='50',Theory2__lte='99.99')).count()
    # total_course=TP.objects.filter('Course_Name')
    # Overall  - CWD
    total_cwd_over_ab=total.filter(Q(Course_Name__icontains="web developer",Practical1__icontains = 'ab')|Q(Course_Name__icontains="web developer",Theory1__icontains = 'ab')|Q(Course_Name__icontains="web developer",Theory2__icontains = 'ab')).count()
    # total_csa_over_fail=total.filter(Q(Course_Name__icontains = "cyber security",Theory2__lt='50',Theory2__gte='0.0')|Q(Course_Name__icontains = "cyber security",Theory1__lt='50',Theory1__gte='0.0')|Q(Course_Name__icontains = "cyber security",Practical1__lt='45',Practical1__gte='0.0')).count()
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
    # total_course=TP.objects.filter('Course_Name')

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
    # total_course=TP.objects.filter('Course_Name')
    print("Total Course :", total_exam,total_cmd,total_cwd,total_caapa,total_deo,total_csa)
     # Theory 01 - CSA
    total_csa_t1_ab=total.filter(Q(Course_Name__icontains="cyber security",Theory1__icontains = 'ab')).count()
    total_csa_t1_fail=total.filter(Q(Course_Name__icontains = "cyber security",Theory1__lt='50',Theory1__gte='0.0')).count()
    total_csa_t1_pass=total.filter(Q(Course_Name__icontains = "cyber security",Theory1__gte='50',Theory1__lte='99.99')).count()
    # total_course=TP.objects.filter('Course_Name')

     # Theory 02 - CSA
    total_csa_t2_ab=total.filter(Q(Course_Name__icontains="cyber security",Theory2__icontains = 'ab')).count()
    total_csa_t2_fail=total.filter(Q(Course_Name__icontains = "cyber security",Theory2__lt='50',Theory2__gte='0.0')).count()
    total_csa_t2_pass=total.filter(Q(Course_Name__icontains = "cyber security",Theory2__gte='50',Theory2__lte='99.99')).count()
    # total_course=TP.objects.filter('Course_Name')

    # Overall  - CSA
    total_csa_over_ab=total.filter(Q(Course_Name__icontains="cyber security",Practical1__icontains = 'ab')|Q(Course_Name__icontains="cyber security",Theory1__icontains = 'ab')|Q(Course_Name__icontains="cyber security",Theory2__icontains = 'ab')).count()

    # total_csa_over_fail=total.filter(Q(Course_Name__icontains = "cyber security",Theory2__lt='50',Theory2__gte='0.0')|Q(Course_Name__icontains = "cyber security",Theory1__lt='50',Theory1__gte='0.0')|Q(Course_Name__icontains = "cyber security",Practical1__lt='45',Practical1__gte='0.0')).count()

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
    return render(request, 'center_home_data.html',locals())
