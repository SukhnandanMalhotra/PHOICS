from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# here UserCreationForm is inbuilt form of django
#  its feature are take password1 and password2
# and check they are similar or not and also check some condition of password



class SignUpPage(UserCreationForm):
    Gender = forms.CharField(max_length=10,required=False,help_text='optional.')
    Email = forms.EmailField(max_length=200,help_text='please enter valid email id')

    class Meta:
        model = User
        fields = ('username','Gender','Email','password1','password2',)
