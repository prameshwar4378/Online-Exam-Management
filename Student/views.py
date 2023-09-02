from django.shortcuts import render,redirect, get_object_or_404
from Institute.models import Exam,Question,Option,UserAnswer,CustomUser,Subjects
from django.contrib import messages

from django.contrib.auth.decorators import login_required, user_passes_test

def is_student(user):
    return user.is_authenticated and hasattr(user, 'is_student') and user.is_student

def student_required(view_func):
    decorated_view_func = login_required(user_passes_test(is_student, login_url='/accounts/login')(view_func))
    return decorated_view_func

def check_exam_started(view_func):
    def wrapper_func(request, *args, **kwargs):
        exam_exist = request.session.get('exam_exist', False)
        exam_id = request.session.get('exam_id')
        if exam_exist:
            messages.warning(request,"Exam Session Exist")
            return redirect(f'/Student/start_exam/{exam_id}')  
        return view_func(request, *args, **kwargs)

    return wrapper_func


def student_profile(request):
    return render(request,"student__student_profile_page.html")

from django.contrib.auth.forms import SetPasswordForm
 
def update_student_password(request):
    id=request.user.id
    user = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        form = SetPasswordForm(user=user, data=request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            messages.success(request,'Password Updated Succesfully')
            return redirect('/Student')
    else:
        form = SetPasswordForm(user=user)
    return render(request, 'student__update_student_password.html', {'form': form})

from django.db.models import Max, Count, F, Q
from django.core.exceptions import ObjectDoesNotExist

@check_exam_started
@student_required
def student_dashboard(request):
    # UserAnswer.objects.filter(exam_id="1").count() 
    try:
        subject_list=Subjects.objects.filter(class_name=request.user.class_name)
        
        latest_user_answer = UserAnswer.objects.filter(student=request.user).latest('id')

        student_id = request.user.id
        exam_id = latest_user_answer.exam.id
        subject_name = latest_user_answer.exam.subject

        total_exams = Exam.objects.filter(is_publish=True,class_name=request.user.class_name,division__contains=request.user.division).count()
        attempted_exams = UserAnswer.objects.filter(student=request.user).values('exam').distinct().count()
        pending_exams = total_exams - attempted_exams 
        exam_dates = []
        exam_percentage = []
        if request.method=="POST":
            if 'subject_name' in request.POST:
                subject_name=request.POST.get('subject_name')
    
        # Calculate the exam percentage for each exam
        exams = Exam.objects.filter(useranswer__student=request.user,subject=subject_name).annotate(
            total_questions=Count('question'),
            correct_answers=Count('useranswer', filter=Q(useranswer__student=request.user, useranswer__selected_option__is_correct=True)),
        )

        for exam in exams:
            if exam.total_questions > 0:
                percentage = (exam.correct_answers / exam.total_questions) * 100
            else:
                percentage = 0

            # Append the exam date and percentage to the lists
            date=exam.exam_date.strftime('%d-%m-%Y')
            exam_dates.append(str(date))
            exam_percentage.append(percentage)


        subject_list_for_progress_graph = []
        percentage_list = []

        # Get the list of subjects for the student's class
        for subject in Subjects.objects.filter(class_name=request.user.class_name):
            subject_list_for_progress_graph.append(subject.subject)

            # Calculate percentage for each exam for the current subject
            exams_for_subject = Exam.objects.filter(subject=subject.subject, is_publish=True)
            total_questions_for_subject = exams_for_subject.aggregate(total_questions=Count('question'))['total_questions']
            correct_answers_for_subject = UserAnswer.objects.filter(student=request.user, exam__in=exams_for_subject, selected_option__is_correct=True).count()

            if total_questions_for_subject > 0:
                percentage_for_subject = (correct_answers_for_subject / total_questions_for_subject) * 100
            else:
                percentage_for_subject = 0

            # Append the percentage for the subject to the percentage_list
            percentage_list.append(percentage_for_subject)
 
        context = {
            'subject_name':subject_name,
            'subject_list':subject_list,
            'subject_list_for_progress_graph':subject_list_for_progress_graph,
            'percentage_list':percentage_list,
            'latest_user_answer': latest_user_answer, 
            'exam_dates_list':exam_dates,
            'exam_percentage_list':exam_percentage,
            'total_exams': total_exams,
            'attempted_exams': attempted_exams,
            'pending_exams': pending_exams,
        }

    except UserAnswer.DoesNotExist:
        # Handle the case when no UserAnswer is found for the student 
        latest_user_answer = None  
        context = {
            'latest_user_answer': latest_user_answer,
            'exam_dates': [],
            'exam_percentage': [],
        }

    return render(request, "student_dashboard.html", context)

@check_exam_started
@student_required
def exam_list(request): 
    # UserAnswer.objects.all().delete()
    runing_exam=False
    exam_id=request.session.get('exam_id')
    exam_name="None" 
    if exam_id:
        exam_name=Exam.objects.get(id=exam_id)
        exam_name=exam_name.name
    if request.session.get('exam_exist'):
        runing_exam=True
    user_submitted_exams = UserAnswer.objects.filter(student_id=request.user.id).values('exam_id')
    remaining_exams = Exam.objects.filter(class_name=request.user.class_name,division__contains=request.user.division,is_publish=True).exclude(id__in=user_submitted_exams)
    return render(request,'student__exam_list.html',{'rec':remaining_exams,"runing_exam":runing_exam,'exam_id':exam_id,'exam_name':exam_name})

import datetime
from django.core.exceptions import ObjectDoesNotExist

@check_exam_started
@student_required
def exam_overview(request, id):
    exam = Exam.objects.get(id=id)
    total_questions = exam.question_set.count()
    exam_duration=str(exam.exam_duration)[0:5] 
    try:
        exam_submitted = UserAnswer.objects.filter(exam=exam, student=request.user).exists()
    except ObjectDoesNotExist:
        exam_submitted = False

    context = {'exam': exam, 'total_questions': total_questions, 'exam_submitted': exam_submitted,'exam_duration':exam_duration}
    return render(request, 'student__exam_overview.html', context)



@student_required
def start_exam(request,exam_id):
    
    if UserAnswer.objects.filter(exam=exam_id,student=request.user):
        messages.warning(request,"Opps You were alredy submited this exam") 
        request.session['exam_exist']=False
        return redirect('/Student/student_exam_list/')
    
    request.session['exam_id'] = exam_id
    questions = Question.objects.filter(exam=exam_id)
    exam=Exam.objects.get(id=exam_id)
    exam_duration=exam.exam_duration
    ex_duration=str(exam_duration)[0:5]
    H=exam_duration.hour
    M=exam_duration.minute
    S=exam_duration.second 

    if not request.session.get('exam_exist'):
        exam_duration = datetime.timedelta(hours=H, minutes=M, seconds=S)
        exam_started_time = datetime.datetime.now().time()
        current_date = datetime.datetime.now().date()
        exam_start_datetime = datetime.datetime.combine(current_date, exam_started_time)
        exam_end_datetime = exam_start_datetime + exam_duration
        expected_end_time = exam_end_datetime.time()
        request.session['exam_started_date_time']=exam_end_datetime.isoformat()
        request.session['exam_exist']=True
    else: 
        exam_started_date_time_iso = request.session.get('exam_started_date_time')
        if exam_started_date_time_iso:
            exam_end_datetime = datetime.datetime.fromisoformat(exam_started_date_time_iso)
    return render(request, 'student__start_exam.html', {'questions': questions,'exam_end_datetime':exam_end_datetime,'exam_duration':ex_duration,'total_questions':questions.count(),'exam':exam})

@student_required
def submit_exam(request):
    student_id = request.user.id
    score = 0
    attempted_questions = 0
    correct_answers = 0
    incorrect_answers = 0

    exam_id = request.session.get('exam_id')
    if not exam_id:
        messages.warning(request,"Select Appropriate Exam...!")
        return redirect('/Student/student_exam_list/')
    
    if UserAnswer.objects.filter(exam=exam_id,student=request.user):
        messages.warning(request,"Opps You were alredy submited this exam") 
        request.session['exam_exist']=False
        return redirect('/Student/student_exam_list/')
    
    exam = Exam.objects.get(id=exam_id)
    for question in Question.objects.filter(exam=exam):
        selected_option = request.POST.get(str(question.id))
        if selected_option:
            attempted_questions += 1
            option = Option.objects.get(id=int(selected_option))
            if option.is_correct:
                score += 1
                correct_answers += 1
            else:
                incorrect_answers += 1

            user = CustomUser.objects.get(id=student_id)
            UserAnswer.objects.create(student=user, exam=exam, question=question, selected_option=option)
        
            request.session['exam_exist']=False
            request.session['exam_id_for_review']=exam_id
            request.session['exam_id']=False

    total_questions = Question.objects.filter(exam=exam).count()
    percentage = (score / total_questions) * 100
    return render(request, 'result.html', {'total_questions': total_questions, 'attempted_questions': attempted_questions, 'correct_answers': correct_answers, 'incorrect_answers': incorrect_answers, 'score': score, 'percentage': percentage})
 
def exam_review(request): 
    user = request.user  # Assuming the user is authenticated
    exam_id=request.session.get('exam_id_for_review')
    exam = get_object_or_404(Exam, id=exam_id)
    exam_reviews = UserAnswer.objects.filter(student=user, exam=exam)

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
    higher_score_users = UserAnswer.objects.filter(
        exam=exam,
        selected_option__is_correct=True,
    ).values('student__id').annotate(score_count=Count('selected_option__is_correct')).filter(score_count__gt=score)
    
    request.session['percentage']=percentage

    return render(request, 'student__exam_review.html', {                                   
        'exam_reviews': exam_reviews,
        'exam_details': exam,
        'score': score,
        'attempted_questions': attempted_questions,
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'total_questions': total_questions,
        'percentage': percentage,
        })

from django.db.models import Count

@check_exam_started
@student_required
def exam_review_using_exam_id(request, exam_id):
    user = request.user  # Assuming the user is authenticated
    exam = get_object_or_404(Exam, id=exam_id)
    exam_reviews = UserAnswer.objects.filter(student=user, exam=exam)

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
    return render(request, 'student__exam_review_using_exam_id.html', {
        'exam_reviews': exam_reviews,
        'exam_details': exam,
        'score': score,
        'attempted_questions': attempted_questions,
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'total_questions': total_questions,
        'percentage': percentage,
        'rank': rank
    })

from django.db.models import Count

@student_required
def result_review_list(request):
    user = request.user.id  # Assuming the user is authenticated
    # Get submitted exams by the student
    submitted_exam_ids = UserAnswer.objects.filter(student_id=user).values_list('exam_id', flat=True)
    # Retrieve available exams and annotate with the number of students who took each exam
    available_exams = Exam.objects.filter(id__in=submitted_exam_ids).annotate(num_students=Count('useranswer'))
    # Sort the exams based on the number of students who took them in descending order
    available_exams = available_exams.order_by('-num_students')

    return render(request, 'student__result_list.html', {'available_exams': available_exams})

@check_exam_started
@student_required
def ranked_in_exam_certificate(request,id):
    exam_data=Exam.objects.get(id=id)
    rank=request.session.get('set_rank_for_certificate')
    current_date = datetime.datetime.now().date()
    return render(request,"certificate/student__rank_certificate.html",{'exam_data':exam_data,'rank':rank,'current_date':current_date})

@check_exam_started
@student_required
def default_exam_certificate(request):
    exam_id=request.session.get('exam_id_for_review')
    percentage=request.session.get('percentage')
    exam_data=Exam.objects.get(id=exam_id) 
    current_date = datetime.datetime.now().date()
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
    return render(request,"certificate/student__default_certificate.html",{'exam_data':exam_data,'current_date':current_date,'percentage':percentage,'grade':grade})



@check_exam_started
@student_required
def download_exam_certificate(request,exam_id):
    user = request.user  # Assuming the user is authenticated
    exam = get_object_or_404(Exam, id=exam_id)
    exam_reviews = UserAnswer.objects.filter(student=user, exam=exam)

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

    exam_data=Exam.objects.get(id=exam_id) 
    current_date = datetime.datetime.now().date()

    print("###################")
    print("###################")
    print("###################")
    print(percentage)
    print(percentage)
    print(percentage)
    print("###################")
    print("###################")
    print("###################")
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
        grade= "E"
    return render(request,"certificate/student__default_certificate.html",{'exam_data':exam_data,'current_date':current_date,'percentage':percentage,'grade':grade})
