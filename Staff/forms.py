from django.contrib.auth.forms import UserCreationForm 
from Institute.models import CustomUser,Exam,Subjects
from django import forms
from django.contrib.auth.forms  import AuthenticationForm
from django.core.exceptions import ValidationError



CLASS=(
    ("","--------"),
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

class Student_Creation_Form(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Confirm Password'})
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    is_student = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox'}), initial=True)
    class Meta:
        model = CustomUser
        fields = ('student_prn_no','username','name','gender','roll_no','password1','password2','is_student')
        widgets={
            'name': forms.TextInput(attrs={'autofocus': True, }), 
        }


class Student_Update_Form(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Confirm Password'})
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
    # class_name = forms.ChoiceField(choices=CLASS)   
    class Meta:
        model = CustomUser
        fields = ('student_prn_no','name','gender', 'roll_no','password1','password2')
        widgets={
            'name': forms.TextInput(attrs={'autofocus': True, }),  
        }

class Form_Create_Exam(forms.ModelForm): 
    class Meta:
        model = Exam
        fields = ('name','exam_date','exam_duration')
        widgets={ 
            'exam_date': forms.TextInput(attrs={'type': 'date'}),
            'exam_duration': forms.TextInput(attrs={'readonly': True }), 
        }
        
        labels = {
            'name': 'Exam Title',  # Change the label here
        }

    def __init__(self, *args, **kwargs):
        super(Form_Create_Exam, self).__init__(*args, **kwargs)
        self.fields['exam_duration'].label = ''
 
class Form_Update_Exam(forms.ModelForm): 
    class Meta:
        model = Exam
        fields = ('name','class_name','subject','exam_date','exam_duration','is_publish','is_result_declared')
        widgets={ 
            'exam_date': forms.TextInput(attrs={'type': 'date'}),
            'exam_duration': forms.TextInput(attrs={'readonly': True }),
            'subject': forms.TextInput(attrs={'readonly': True }),
            'class_name': forms.TextInput(attrs={'readonly': True }),
        }
    def __init__(self, *args, **kwargs):
        super(Form_Update_Exam, self).__init__(*args, **kwargs)
        self.fields['exam_duration'].label = ''
   
 
 
class Form_Subjects(forms.ModelForm): 
    class Meta:
        model = Subjects
        fields = ('subject','class_name')
        widgets={
        'class_name': forms.TextInput(attrs={'readonly': True }),
        }