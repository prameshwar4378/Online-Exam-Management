from django.db import models

from django.contrib.auth.models import AbstractUser

CLASS=(
    ("No Class Teacher","No Class Teacher"),
    ("1st","1st"),
    ("2nd","2nd"),
    ("3rd","3rd"),
    ("4th","4th"),
    ("5th","5th"),
    ("6th","6th"),
    ("7th","7th"),
    ("8th","8th"),
    ("9th","9th"),
    ("10th","10th"),
)

DIVISION=(
    ("Azalea","Azalea"),
    ("Zinnia","Zinnia"),
    ("Camelia","Camelia"),
)

GENDER=(
    ("Male","Male"),
    ("Female","Female"),
)

class Subjects(models.Model):
    subject=models.CharField(max_length=50)
    class_name=models.CharField(max_length=50)

class CustomUser(AbstractUser):
    # Genaral fields 
    student_prn_no = models.BigIntegerField(null=True,unique=True)
    name = models.CharField(max_length=200,null=True)
    roll_no = models.CharField(max_length=20,null=True)
    class_name = models.CharField(max_length=50,null=True,choices=CLASS)
    division = models.CharField(max_length=10,null=True,choices=DIVISION)
    is_institute=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_student=models.BooleanField(default=False)
    staff_id = models.CharField(max_length=10,null=True)
    designation=models.CharField(max_length=50,null=True,blank=True)
    email=models.EmailField(max_length=254,null=True,blank=True)
    gender=models.CharField(max_length=50,null=True,blank=True,choices=GENDER)
    def __str__(self):
        return self.username

class Exam(models.Model):
    name = models.CharField(max_length=200,null=True)
    subject = models.CharField(max_length=50,null=True)
    exam_date = models.DateField()
    exam_duration = models.TimeField(null=True)
    class_name = models.CharField(max_length=50,null=True,choices=CLASS)
    division = models.CharField(max_length=10,null=True,choices=DIVISION)
    is_publish = models.BooleanField(default=False)
    is_result_declared = models.BooleanField(default=False)
    staff_id = models.CharField(max_length=50,null=True)
    record_created_date=models.DateField(auto_now=False, auto_now_add=True, null=True)
    def __str__(self):
        return self.name
    
class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE,null=True)
    question_text = models.CharField(max_length=1000)

    def __str__(self):
        return self.question_text

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text


class UserAnswer(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE,null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE,null=True)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"{self.student} - {self.question}"