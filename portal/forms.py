from django import forms
from datetime import datetime

# from django.forms.widgets import RadioSelect
from portal.models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        status = forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()), empty_label=None)
        size = forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()), empty_label=None)
        flip = forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()), empty_label=None)
        rotate= forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()),empty_label=None)
        blur=forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()), empty_label=None)
        effect = forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()), empty_label=None)
        fields = ('document', 'status', 'size', 'flip', 'rotate', 'blur', 'effect')

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Document
        status = forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()), empty_label=None)
        size = forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()), empty_label=None)
        flip = forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()), empty_label=None)
        rotate = forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()), empty_label=None)
        blur = forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()), empty_label=None)
        effect = forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()), empty_label=None)

        fields = ('status', 'size', 'flip', 'rotate', 'blur', 'effect')

class ResetForm(forms.ModelForm):
    class Meta:
        model = Document
        reset=forms.ModelChoiceField(queryset=Document.objects.filter(uploaded_at=datetime.now()), empty_label=None)

        fields= ('reset',)













