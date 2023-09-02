from django.shortcuts import render, redirect
from .forms import Student_Creation_Form,Student_Update_Form,Form_Create_Exam,Form_Update_Exam,Form_Subjects
from django.contrib import messages
from Institute.models import CustomUser,Exam,Question,Option,UserAnswer,Subjects
 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import cache_page


def is_staff(user):
    return user.is_authenticated and hasattr(user, 'is_staff') and user.is_staff

def staff_required(view_func):
    decorated_view_func = login_required(user_passes_test(is_staff, login_url='/accounts/login')(view_func))
    return decorated_view_func

def my_exam_list_object_for_base(request):
    if request.user.is_authenticated:
        exam = Exam.objects.filter(staff_id=request.user.staff_id).order_by('-id')
    else:
        exam={}
    return {'exam_list_data': exam}

def staff_profile(request):
    return render(request,"staff__staff_profile_page.html")

from django.contrib.auth.forms import SetPasswordForm
 
def update_staff_password(request):
    id=request.user.id
    user = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        form = SetPasswordForm(user=user, data=request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            messages.success(request,'Password Updated Succesfully')
            return redirect('/Staff')
    else:
        form = SetPasswordForm(user=user)
    return render(request, 'staff__update_staff_password.html', {'form': form})


@staff_required
def staff_dashboard(request): 
    # CustomUser.objects.filter(is_staff=False).delete()
    students=CustomUser.objects.filter(is_student=True,class_name=request.user.class_name,division=request.user.division)
    student_count=students.count()
    boys=CustomUser.objects.filter(is_student=True,gender="Male",class_name=request.user.class_name,division=request.user.division)
    boys_count=boys.count()
    girls=CustomUser.objects.filter(is_student=True,gender="Female",class_name=request.user.class_name,division=request.user.division)
    girls_count=girls.count()
    
    subjects=Subjects.objects.filter(class_name=request.user.class_name)
    subject_list=[]
    for i in subjects:
        subject_list.append(i.subject)
    exam_status_labels=['total_exams','attended_exams','pending_exam']
    exam_status_data=[]
    total_exams = Exam.objects.filter(class_name=request.user.class_name, division__contains=request.user.division).count()
    attended_exams=UserAnswer.objects.filter( ).values('student').distinct().count()
    pending_exam=int(total_exams)-int(attended_exams)
    exam_status_data.append(total_exams)
    exam_status_data.append(attended_exams)
    exam_status_data.append(pending_exam)

    gender_list=['boys','girls'] 
    student_count_list=[]
    student_count_list.append(boys_count) 
    student_count_list.append(girls_count)
   
    subject_name=None
    if request.method=="POST":
        if 'subject_name' in request.POST:
            subject_name=request.POST.get('subject_name')
     
    context={
        'exam_status_labels':exam_status_labels,
        'exam_status_data':exam_status_data,
        'student_count':student_count,
        'boys_count':boys_count,
        'gender_list':gender_list,
        'student_count_list':student_count_list,
        'girls_count':girls_count,
        'subject_name':subject_name,  
        'subject_list':subject_list,   
        }
    return render(request,"staff_dashboard.html",context)

from django.db.models import Max

@staff_required
def add_student(request): 
    try:
        largest_prn_no = CustomUser.objects.exclude(student_prn_no__isnull=True).order_by('-student_prn_no').first()
    except CustomUser.DoesNotExist:
        largest_prn_no = None

    if largest_prn_no is None:
        largest_prn_no = 2023240001

    if isinstance(largest_prn_no, CustomUser):
        auto_student_prn_no = int(largest_prn_no.student_prn_no) + 1
    else:
        auto_student_prn_no = largest_prn_no

    student_prn_numbers_list = CustomUser.objects.values_list('student_prn_no', flat=True)

    is_available = auto_student_prn_no in student_prn_numbers_list
    while is_available:
        auto_student_prn_no += 1
        is_available = auto_student_prn_no in student_prn_numbers_list

    print("Auto Student PRN No:", auto_student_prn_no)

    if request.method == 'POST':
        form = Student_Creation_Form(request.POST, request.FILES)
        if form.is_valid():
            fm1 = form.save(commit=False)
            fm1.class_name = request.user.class_name 
            fm1.division = request.user.division 
            form.save()
            messages.success(request,'Student Added Successfully ...!')
            return redirect('/Staff/add_student/')
    else:
        form = Student_Creation_Form()
    return render(request, 'staff__add_student.html', {'form': form,'auto_student_prn_no':auto_student_prn_no})
 
@staff_required
def student_list(request): 
    rec=CustomUser.objects.filter(is_student=True,class_name=request.user.class_name,division=request.user.division).order_by('-id')
    return render(request,'staff__student_list.html',{'rec':rec})


@staff_required
def update_student(request,id):
    if request.method=="POST":
        pi=CustomUser.objects.get(pk=id)
        fm=Student_Update_Form(request.POST,request.FILES, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Student Updated Successfully')
            return redirect('/Staff/student_list/')
    else:
        pi=CustomUser.objects.get(pk=id)
        fm=Student_Update_Form(instance=pi)
    return render(request,'staff__update_student.html',{'form':fm})


@staff_required
def create_exam(request): 
    class_names_list = ["1st","2nd","3rd","4th","5th","6th","7th","8th","9th","10th"] 
    subject_list=request.session.get('get_subjects_list')
    session_class_name_for_exam=request.session.get('class_name_for_exam')
    
    if request.method == 'POST':
        form = Form_Create_Exam(request.POST, request.FILES)
        if form.is_valid():
            fm1 = form.save(commit=False)
            fm1.staff_id = request.user.staff_id
            selected_divisions = request.POST.getlist('division')
            divisions_string = "|".join(selected_divisions)
            fm1.division = divisions_string
            fm1.subject=request.POST.get('subject')
            fm1.class_name=session_class_name_for_exam
            form.save()
            messages.success(request, 'Exam Created Successfully ...!')
            request.session['class_name_for_exam'] = []
            request.session['get_subjects_list'] = []
            return redirect('/Staff/create_exam/')
    else:
        form = Form_Create_Exam()
    return render(request, 'staff__create_exam.html', {'form': form,'subject_list':subject_list,'session_class_name_for_exam':session_class_name_for_exam,'class_names_list':class_names_list})
  
def send_class_name_for_subject_create_exam(request):
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        class_objects = Subjects.objects.filter(class_name=class_name)
        subject_list=[]
        for i in class_objects:
            subject_list.append(i.subject)
        request.session['class_name_for_exam'] = class_name
        request.session['get_subjects_list'] = subject_list
    return redirect('/Staff/create_exam')

@staff_required
def update_exam(request, id):
    if request.method == "POST":
        exam_instance = Exam.objects.get(pk=id)
        form = Form_Update_Exam(request.POST, request.FILES, instance=exam_instance)
        if form.is_valid():
            exam = form.save(commit=False)
            selected_divisions = request.POST.getlist('division')
            divisions_string = "|".join(selected_divisions)
            exam.division = divisions_string
            exam.save()
            messages.success(request, 'Exam Updated Successfully')
            return redirect('/Staff/staff_exam_list/')
    else:
        exam_instance = Exam.objects.get(pk=id)
        form = Form_Update_Exam(instance=exam_instance)

        # Get the previously selected divisions for the exam
        previous_divisions = exam_instance.division.split("|") if exam_instance.division else []

    return render(request, 'staff__update_exam.html', {'form': form,'previous_divisions':previous_divisions,'exam_data':exam_instance})

 
@staff_required
def add_subject(request):
    subject=Subjects.objects.filter(class_name=request.user.class_name)
    print()
    if request.method == 'POST':
        form = Form_Subjects(request.POST, request.FILES)
        if form.is_valid(): 
            form.save()
            messages.success(request, 'Subject Added Successfully ...!')
            return redirect('/Staff/add_subject/')
    else:
        form = Form_Subjects()
    return render(request, 'staff__manage_subjects.html', {'form': form,'subject':subject})


@staff_required
def update_subject(request, id):
    if request.method == "POST":
        subject_instance = Subjects.objects.get(pk=id)
        form = Form_Subjects(request.POST, request.FILES, instance=subject_instance)
        if form.is_valid():  
            form.save()
            messages.success(request, 'Subject Updated Successfully')
            return redirect('/Staff/add_subject/')
    else:
        exam_instance = Subjects.objects.get(pk=id)
        form = Form_Subjects(instance=exam_instance)
    return render(request, 'staff__update_exam.html', {'form': form})

@staff_required
def delete_subject(request,id):
        pi=Subjects.objects.get(pk=id)
        pi.delete()
        messages.success(request,'Subject Deleted Successfully!!!')
        return redirect('/Staff/add_subject/')

from .filters import Exam_List_Filter
@staff_required
def staff_exam_list(request): 
    record=Exam.objects.filter(staff_id=request.user.staff_id).order_by('-exam_date')
    Filter=Exam_List_Filter(request.GET, queryset=record)
    rec=Filter.qs 
    base_url = request.scheme + "://" + request.get_host()
    exam_url=f"{base_url}/Student/exam_overview/"
    return render(request,'staff__exam_list.html',{'rec':rec,'filter':Filter,"exam_url":exam_url})

@staff_required
def delete_exam(request,id):
        pi=Exam.objects.get(pk=id)
        pi.delete()
        messages.success(request,'Exam Deleted Successfully!!!')
        return redirect('/Staff/staff_exam_list/')

@staff_required
def delete_student(request,id):
        pi=CustomUser.objects.get(pk=id)
        pi.delete()
        messages.success(request,'Student Deleted Successfully!!!')
        return redirect('/Staff/student_list/')

from django.shortcuts import render, get_object_or_404

@staff_required
def create_question(request):
    exam_id = request.session.get('exam_id')
    exam_record = get_object_or_404(Exam, id=exam_id)
    questions_record = Question.objects.filter(exam=exam_record)

    request.session['exam_id_for_delete_question_redirect'] = exam_id  

    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        options = request.POST.getlist('option_text')
        correct_answer = request.POST.get('correct_answer')

        question = Question(exam=exam_record, question_text=question_text)
        question.save()

        for i, option in enumerate(options):
            is_correct = False
            if str(i) == correct_answer:
                is_correct = True
            Option.objects.create(question=question, option_text=option, is_correct=is_correct)

    exam_details = Question.objects.filter(exam=exam_record)

    context = {'exam_details': exam_details, 'exam': exam_record, 'questions': questions_record}
    return render(request, 'mcq_exam/create_question.html', context)

@staff_required
def select_exam_for_create_question(request):
    if request.method == 'POST':
        exam_id = request.POST.get('exam_id') 
        request.session['exam_id'] = exam_id
    return redirect('/Staff/create_question')

@staff_required
def select_exam_for_exam_dashboard(request):
    if request.method == 'POST':
        exam_id = request.POST.get('exam_id')  
    return redirect(f'/Staff/exam_dashboard/{exam_id}')
 
# def exam_dashboard(request, exam_id):
#     UserAnswer.objects.all().delete()
#     try:
#         exam = Exam.objects.get(id=exam_id)
#     except Exam.DoesNotExist:
#         messages.warning(request,"Exam Not Found")
#         return redirect("/Staff")
#     divisions = exam.division.split('|')
#     students = CustomUser.objects.filter(is_student=True, class_name=exam.class_name, division__in=divisions)
#     attempted_students = CustomUser.objects.filter(useranswer__exam=exam)
#     context = {
#         'exam': exam,
#         'students': students,
#         'attempted_students': attempted_students,
#     }
    
#     return render(request, "staff__exam_dashboard.html", context)




@staff_required
def exam_dashboard(request, exam_id):
    try:
        exam = Exam.objects.get(pk=exam_id)
    except Exam.DoesNotExist:
        messages.warning(request, "Exam Not Exist")
        return redirect("/Staff")

    divisions = exam.division.split('|')
    students = CustomUser.objects.filter(is_student=True, class_name=exam.class_name, division__in=divisions)
    total_students=students.count()
    # Calculate student percentage and attendance for the exam
    attended_students = 0
    total_percentage = 0.0
    
    for student in students:
        student.percentage = calculate_student_percentage(exam, student)
        student.attended = has_student_attained_exam(student, exam)

        if student.attended:
            attended_students += 1
            total_percentage += student.percentage

    not_attended_students = len(students) - attended_students

    # Calculate average percentage
    if attended_students > 0:
        average_percentage = total_percentage / attended_students
    else:
        average_percentage = 0.0

    # Sort students by percentage (descending order)
    students = sorted(students, key=lambda student: student.percentage, reverse=True)

    context = {
        'exam_id': exam_id,
        'exam': exam,
        'students': students,
        'total_students':total_students,
        'attended_students': attended_students,
        'not_attended_students': not_attended_students,
        'average_percentage': average_percentage,
    }
    return render(request, 'exam_dashboard.html', context)

def calculate_student_percentage(exam, student): 
    total_questions = exam.question_set.count()
    total_correct_answers = UserAnswer.objects.filter(exam=exam, student=student, selected_option__is_correct=True).count()
    maximum_marks = total_questions
    if total_questions == 0:
        return 0.0
    percentage = (total_correct_answers / maximum_marks) * 100
    return round(percentage, 2)

def has_student_attained_exam(student, exam):
    # Your logic to check if the student has attended the exam
    # Replace this with your actual logic based on exam and student data
    return UserAnswer.objects.filter(student=student, exam=exam).exists()

from django.template.loader import get_template
from django.http import HttpResponse
from io import BytesIO
from xhtml2pdf import pisa 

@staff_required
def export_exam_data_to_pdf(request, exam_id):
    template = get_template('staff__export_exam_data.html')
    try:
        exam = Exam.objects.get(pk=exam_id)
    except Exam.DoesNotExist:
        messages.warning(request, "Exam Not Exist")
        return redirect("/Staff")

    divisions = exam.division.split('|')
    students = CustomUser.objects.filter(is_student=True, class_name=exam.class_name, division__in=divisions)

    # Calculate student percentage and attendance for the exam
    attended_students = 0
    total_percentage = 0.0
    
    for student in students:
        student.percentage = calculate_student_percentage(exam, student)
        student.attended = has_student_attained_exam(student, exam)

        if student.attended:
            attended_students += 1
            total_percentage += student.percentage

    not_attended_students = len(students) - attended_students

    # Calculate average percentage
    if attended_students > 0:
        average_percentage = total_percentage / attended_students
    else:
        average_percentage = 0.0

    # Sort students by percentage (descending order)
    students = sorted(students, key=lambda student: student.percentage, reverse=True)

    context = {
        'exam': exam,
        'students': students,
        'attended_students': attended_students,
        'not_attended_students': not_attended_students,
        'average_percentage': average_percentage,
    }  
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{exam.name}.pdf"'
    pdf = pisa.CreatePDF(BytesIO(html.encode('utf-8')), response)
    if not pdf.err:
        return response
    return HttpResponse('Error generating PDF file: %s' % pdf.err, status=400)



from django.db.models import Count

@staff_required
def student_individual_exam_review(request, exam_id, student_id):
    student = student_id  # Assuming the user is authenticated
    exam = get_object_or_404(Exam, id=exam_id)
    exam_reviews = UserAnswer.objects.filter(student=student, exam=exam)

    score = 0
    attempted_questions = 0
    correct_answers = 0
    incorrect_answers = 0
    total_questions = exam_reviews.count()

    for exam_review in exam_reviews:
        attempted_questions += 1
        if exam_review.selected_option.is_correct:
            score += 1
            correct_answers += 1
        else:
            incorrect_answers += 1

    percentage = round((score / total_questions) * 100, 2)

    # Retrieve users with higher scores than the authenticated user for the same exam
    higher_score_users = UserAnswer.objects.filter(
        exam=exam,
        selected_option__is_correct=True,
    ).values('student__id').annotate(score_count=Count('selected_option__is_correct')).filter(score_count__gt=score)

    # Calculate the rank of the authenticated user
    rank = higher_score_users.count() + 1
    request.session['set_rank_for_certificate']=rank

    if percentage >= 90:
        grade= "A++"
    elif 80 <= percentage < 90:
        grade= "A+"
    elif 70 <= percentage < 80:
        grade= "B++"
    elif 60 <= percentage < 70:
        grade= "B+"
    elif 50 <= percentage < 60:
        grade= "C++"
    elif 40 <= percentage < 50:
        grade= "C+"
    elif 30 <= percentage < 40:
        grade= "D" 
    else:
        grade= "Fail" 

    return render(request, 'staff__student_individual_exam_review.html', {
        'exam_reviews': exam_reviews,
        'exam_details': exam,
        'score': score,
        'attempted_questions': attempted_questions,
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'total_questions': total_questions,
        'percentage': percentage,
        'rank': rank,
        'grade':grade
    })


@staff_required
def delete_submited_exam(request, student_id, exam_id):
    UserAnswer.objects.filter(student_id=student_id,exam_id=exam_id).delete()
    student_name=CustomUser.objects.get(id=student_id)
    messages.success(request,f"Now {student_name.name} Apear for retake exam")
    return redirect(f"/Staff/exam_dashboard/{exam_id}")

@staff_required
def delete_Question(request,id):
    Question.objects.filter(id=id).delete() 
    exam_id=request.session.get('exam_id_for_delete_question_redirect')
    messages.success(request,"Question Successfuly deleted")
    return redirect("/Staff/create_question/")