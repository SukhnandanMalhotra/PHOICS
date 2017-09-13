from django import forms

from portal.models import Document

STATUS_CHOICES = ((1, "Private"),(2, "public"),)

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        status = forms.ChoiceField(choices=STATUS_CHOICES, label="Choose private or public as you want your photo to be ", initial='', widget=forms.RadioSelect(), required=True)
        fields = ( 'document','status')
