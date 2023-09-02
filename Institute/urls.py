
from django.urls import path,include
from Institute import views
urlpatterns = [
    path("",views.institute_dashboard,name="institute_dashboard"), 
    path("add_staff/",views.add_staff,name="add_staff"), 
    path("staff_list/",views.staff_list,name="staff_list"), 
    path("update_staff/<int:id>",views.update_staff,name="update_staff"), 
    path("institute_staff_dashboard/<int:id>",views.institute_staff_dashboard,name="institute_staff_dashboard"), 
    path("institute_staff_exam_list/<int:id>",views.staff_exam_list,name="institute_staff_exam_list"), 
    path("institute__exam_question_ans_review/<int:id>",views.institute__exam_question_ans_review,name="institute__exam_question_ans_review"), 
    path("student_bulk_registration/",views.student_bulk_registration,name="student_bulk_registration"), 
    path("export_students/",views.export_students,name="export_students"), 
    path("export_staff/",views.export_staff,name="export_staff"), 
    path("institute_update_student/<int:id>",views.institute_update_student,name="institute_update_student"), 
    path("student_list/",views.student_list,name="institute_student_list"), 
    path("exam_list/",views.exam_list,name="exam_list"), 
]
