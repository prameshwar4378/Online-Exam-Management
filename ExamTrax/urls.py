"""
URL configuration for ExamTrax project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
 
from django.contrib import admin
from django.urls import path,include

from Staff import urls as Staff_Urls
from Student import urls as Student_Urls
from Institute import urls as Institute_Urls
from Institute import views as Institute_Views
from Developer import urls as Developer_Urls

urlpatterns = [
    path("",Institute_Views.index,name="index"),
    path('admin/', admin.site.urls),
    path("Staff/",include(Staff_Urls)), 
    path("Student/",include(Student_Urls)), 
    path("Institute/",include(Institute_Urls)), 
    path("Developer/",include(Developer_Urls)), 
    path("accounts/login/",Institute_Views.login,name="login"),
    path("logout/",Institute_Views.logout,name="logout")
]

