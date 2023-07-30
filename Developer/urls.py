
from django.urls import path,include
from Developer import views
urlpatterns = [
    path("",views.developer_dashboard,name="developer_dashboard"),  
    path("institute_registration/",views.institute_registration,name="institute_registration"),  
    path("update_institute/<int:id>",views.update_institute,name="update_institute"),  
    path("institute_list/",views.institute_list,name="institute_list"),  
]