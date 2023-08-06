from django.shortcuts import render
from Institute.models import CustomUser
from .forms import Institute_Registration,Update_institute_Form
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
def developer_dashboard(request):
    return render(request,"developer__developer_dashboard.html")

# Create your views here.
def institute_list(request):
    institute=CustomUser.objects.filter(is_institute=True)
    return render(request,"developer__institute_list.html",{'institute':institute})

def institute_registration(request):
    if request.method == 'POST':
        form = Institute_Registration(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Institute Created Successfully ...!')
            return redirect('/accounts/login/')
    else:
        form = Institute_Registration()
    return render(request, 'developer__add_institute.html', {'form': form})
 

  
def update_institute(request,id):
    if request.method=="POST":
        pi=CustomUser.objects.get(pk=id)
        fm=Update_institute_Form(request.POST,request.FILES, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Institute Updated Successfully') 
    else:
        pi=CustomUser.objects.get(pk=id)
        fm=Update_institute_Form(instance=pi)
    return render(request,'developer__update_institute.html',{'form':fm})   