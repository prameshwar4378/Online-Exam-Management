from django.shortcuts import render, redirect
from .forms import Staff_Creation_Form,Staff_Update_Form,login_form
from django.contrib import messages
from .models import CustomUser,Exam,Question
from django.contrib.auth import login as authlogin, authenticate,logout as DeleteSession
from .filters import Exam_List_Filter
from django.contrib.auth.decorators import login_required, user_passes_test

def is_institute(user):
    return user.is_authenticated and hasattr(user, 'is_institute') and user.is_institute

def institute_required(view_func):
    decorated_view_func = login_required(user_passes_test(is_institute, login_url='/accounts/login')(view_func))
    return decorated_view_func

def login(request): 
    lg_form=login_form()
    if request.method=='POST':
        if 'txt_sign_in_username' in request.POST: 
            username = request.POST.get('txt_sign_in_username', False)
            password = request.POST.get('txt_sign_in_password', False)
            user=authenticate(request,username=username,password=password)
            if user is not None:
                authlogin(request,user)
                if user.is_institute==True:
                    return redirect('/Institute',{'user',user}) 
                elif user.is_staff==True:
                    return redirect('/Staff',{'user',user})
                elif user.is_student==True:
                    return redirect('/Student',{'user',user})
            else:
                lg_form=login_form()
                messages.warning(request,'Opps...! User does not exist... Please try again..!')
    return render(request,'login.html',{'form':lg_form})


def logout(request):
    DeleteSession(request)
    return redirect('/accounts/login')


# Create your views here.
def index(request):
    return render(request,"index.html")

from datetime import date, timedelta
# Create your views here.
@institute_required
def institute_dashboard(request):

    total_exams = Exam.objects.count()
    last_30_days = date.today() - timedelta(days=30)

    exams_last_30_days = Exam.objects.filter(exam_date__gte=last_30_days).count()
    last_7_days = date.today() - timedelta(days=30)
    exams_last_7_days = Exam.objects.filter(exam_date__gte=last_7_days).count()

    class_names = ["1st","2nd","3rd","4th","5th","6th","7th","8th","9th","10th"] 
    exam_count = []
    for class_name in class_names:
        count = Exam.objects.filter(class_name=class_name).count()
        exam_count.append(count) 

    student_gender=['Male','Female']
    male_count = CustomUser.objects.filter(gender='Male').count()
    female_count = CustomUser.objects.filter(gender='Female').count()
    students_count = [male_count, female_count] 


    context={
        'total_exams':total_exams,
        'exams_last_30_days':exams_last_30_days,
        'exams_last_7_days':exams_last_7_days,
        'class_names':class_names,
        'exam_count':exam_count,
        'student_gender':student_gender,
        'students_count':students_count,
    }
    return render(request,"institute_dashboard.html",context)

# Create your views here.
@institute_required
def institute_staff_dashboard(request,id):
    profile=CustomUser.objects.get(id=id)
    total_exams = Exam.objects.filter(staff_id=profile.staff_id).count()
    total_published_exams = Exam.objects.filter(staff_id=profile.staff_id, is_publish=True).count()
    total_result_declared_exams = Exam.objects.filter(staff_id=profile.staff_id, is_result_declared=True).count()
    total_student_in_class=CustomUser.objects.filter(class_name=profile.class_name,division=profile.division,is_student=True).count()
    context={
        'profile':profile,
        'total_exams':total_exams,
        'total_student_in_class':total_student_in_class,
        'total_published_exams':total_published_exams,
        'total_result_declared_exams':total_result_declared_exams
    }
    return render(request,"institute_staff_dashboard.html",context)

from django.db.models import Max

@institute_required
def add_staff(request):
    if CustomUser.objects.exclude(staff_id__isnull=True).exists():
        # Calculate the largest_staff_id using existing staff_id values
        largest_staff_id = CustomUser.objects.exclude(staff_id__isnull=True).aggregate(Max('staff_id'))['staff_id__max']
    else:
        # If no CustomUser objects have a non-null staff_id, set the largest_staff_id as "smis-101"
        largest_staff_id = "smis-100"

    staff_id_numbers_list = CustomUser.objects.values_list('staff_id', flat=True)

    split_parts = largest_staff_id.split("-")
    large_number = split_parts[1]
    auto_number=int(large_number)+1

    auto_staff_id=f'smis-{(auto_number)}'

    is_available = auto_staff_id in staff_id_numbers_list
    while is_available:
        auto_number+=1

    print(auto_staff_id)

    if request.method == 'POST':
        form = Staff_Creation_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Staff Added Successfully ...!')
            return redirect('/Institute/add_staff/')
    else:
        form = Staff_Creation_Form()
    context={
        'form': form,
        'auto_staff_id':auto_staff_id,
    }
    return render(request, 'institute__add_staff.html',context)
 
@institute_required
def staff_list(request):
    rec=CustomUser.objects.filter(is_staff=True)
    return render(request,'institute__staff_list.html',{'rec':rec})

@institute_required
def staff_exam_list(request,id):
    staff_profile=CustomUser.objects.get(id=id)
    exam=Exam.objects.filter(staff_id=staff_profile.staff_id)
    Filter=Exam_List_Filter(request.GET, queryset=exam)
    exam_record=Filter.qs 
    context={
        'staff_profile':staff_profile,
        'exam_record':exam_record,
        'filter':Filter,
    }
    return render(request,'institute__staff_exam_list.html',context)

@institute_required
def update_staff(request,id):
    if request.method=="POST":
        pi=CustomUser.objects.get(pk=id)
        fm=Staff_Update_Form(request.POST,request.FILES, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Staff Updated Successfully')
            return redirect('/Institute/staff_list/')
    else:
        pi=CustomUser.objects.get(pk=id)
        fm=Staff_Update_Form(instance=pi)
    return render(request,'institute__update_staff.html',{'form':fm})



from django.shortcuts import render, get_object_or_404
 
def institute__exam_question_ans_review(request,id): 
    exam_record = get_object_or_404(Exam, id=id)
    questions_record = Question.objects.filter(exam=exam_record)
    exam_details = Question.objects.filter(exam=exam_record)
    context = {'exam_details': exam_details, 'exam': exam_record, 'questions': questions_record}
    return render(request, 'institute__exam_question_ans_review.html', context)
