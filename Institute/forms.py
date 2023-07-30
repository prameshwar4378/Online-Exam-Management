from django.contrib.auth.forms import UserCreationForm 
from .models import CustomUser,Subjects 
from django import forms
from django.contrib.auth.forms  import AuthenticationForm
from django.core.exceptions import ValidationError


class Institute_Registration(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Confirm Password'})
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        
    is_institute = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox'}), initial=True)
    class Meta:
        model = CustomUser
        fields = ('username','name','password1','password2','is_institute')
 

CLASS=(
    ("","---------"),
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

class Staff_Creation_Form(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Confirm Password'})
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    class_name = forms.ChoiceField(choices=CLASS, initial='---------')   
    is_staff = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox'}), initial=True)
    class Meta:
        model = CustomUser
        fields = ('username','name','gender','class_name','division','designation','email','staff_id','is_staff','password1','password2')
        widgets={ 
            'staff_id': forms.TextInput(attrs={'readonly': True }), 
        }


 
class Staff_Update_Form(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Confirm Password'})
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
    class_name = forms.ChoiceField(choices=CLASS)   
    class Meta:
        model = CustomUser
        fields = ('name','gender','class_name','division','designation','email','staff_id','is_staff','password1','password2')
        widgets={ 
            'staff_id': forms.TextInput(attrs={'readonly': True }), 
        } 
 
class login_form(AuthenticationForm):
    username=forms.CharField(label='username',widget=forms.TextInput(attrs={'class':'input100','placeholder':'Enter Username'}))
    password=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'input100','placeholder':'Enter Password'}))
 
 