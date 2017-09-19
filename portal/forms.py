from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime
from portal.models import Document
"""
UserCreationForm contain passward1 and password2(conf.password)
it also check both password must be same
"""
class SignUpPage(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class ForgetPassword(forms.Form):
    your_email = forms.EmailField(max_length=254, help_text='Required. Please enter a valid email address')

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=10)

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        status=forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()),empty_label=None)
        fields = ( 'document','status')

class YourNewPassword(forms.Form):
    your_user_name = forms.CharField(max_length=222,)
    old_password = forms.CharField(max_length=222,)
    new_password = forms.CharField(max_length=222,)
