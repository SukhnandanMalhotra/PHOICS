from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpPage(UserCreationForm):
    Gender = forms.CharField(max_length=10,required=False,help_text='optional.')
    Email = forms.EmailField(max_length=200,help_text='please enter valid email id')

    class meta:
        model = User
        fields = ('username','Gender','Email','password1','password2',)
