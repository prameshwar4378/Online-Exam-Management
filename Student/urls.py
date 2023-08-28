
from django.urls import path,include
from Student import views
urlpatterns = [
    path("",views.student_dashboard,name="student_dashboard"),  
    path("student_profile/",views.student_profile,name="student_profile"), 
    path("update_student_password/",views.update_student_password,name="update_student_password"), 
    path("student_exam_list/",views.exam_list,name="student_exam_list"),  
    path("start_exam/<int:exam_id>",views.start_exam,name="start_exam"),  
    path("submit_exam/",views.submit_exam,name="submit_exam"),  
    path("exam_review/",views.exam_review,name="exam_review"),  
    path("exam_review_using_exam_id/<int:exam_id>",views.exam_review_using_exam_id,name="exam_review_using_exam_id"),  
    path("result_review_list/",views.result_review_list,name="result_review_list"),  
    path("ranked_in_exam_certificate/<int:id>",views.ranked_in_exam_certificate,name="ranked_in_exam_certificate"),  
    path("default_exam_certificate/",views.default_exam_certificate,name="default_exam_certificate"),  
    path("exam_overview/<int:id>",views.exam_overview,name="exam_overview"),  
    path("download_exam_certificate/<int:exam_id>",views.download_exam_certificate,name="download_exam_certificate"),  
]