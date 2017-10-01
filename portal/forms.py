from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime
from portal.models import Document, Profile


"""
UserCreationForm contain password1 and password2(conf.password)
it also check both password must be same
"""


class SignUpPage(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class Info(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('First_Name', 'Last_Name', 'City', 'DOB', 'profile_pic', )


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        status = forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()), empty_label=None)
        size = forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()), empty_label=None)
        flip = forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()), empty_label=None)
        rotate = forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()), empty_label=None)
        blur = forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()), empty_label=None)
        effect = forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()), empty_label=None)
        fields = ('document', 'status', 'size', 'flip', 'rotate', 'blur', 'effect')


class UpdateForm(forms.ModelForm):

    class Meta:
        model = Document
        status = forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()),
                                        empty_label=None)
        size = forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()), empty_label=None)
        flip = forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()),
                                      empty_label=None)
        rotate = forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()),
                                        empty_label=None)
        blur = forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()),
                                      empty_label=None)
        effect = forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()),
                                        empty_label=None)
        fields = ('status', 'size', 'flip', 'rotate', 'blur', 'effect')


# class ResetForm(forms.ModelForm):
#     class Meta:
#         model = Document
#         reset = forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()), empty_label=None)
#         fields = ('reset',)

