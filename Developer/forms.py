from django.contrib.auth.forms import UserCreationForm 
from Institute.models import CustomUser,Subjects 
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
 
 
class Update_institute_Form(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Confirm Password'})
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        
    class Meta:
        model = CustomUser
        fields = ('name','password1','password2' )
 

