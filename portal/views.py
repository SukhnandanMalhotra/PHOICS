from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django import forms
from datetime import datetime
from portal.models import Document
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from .models import Document
from .forms import DocumentForm , UpdateForm

from django.forms import ModelForm


def home(request):
     documents = Document.objects.order_by()
     return render(request,'portal/profile.html', { 'documents': documents })


def newsfeed(request):
    documents = Document.objects.all()
    return render(request, 'portal/newsfeed.html', {'documents': documents})


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = DocumentForm()
    return render(request, 'portal/model_form_upload.html', {
        'form': form
    })

def Doc_update(request, pk, template_name='portal/model_form_upload.html'):
    updatex = get_object_or_404(Document, pk=pk)
    form = UpdateForm(request.POST or None, instance=updatex)
    if form.is_valid():
        form.save()
        return redirect('profile')
    return render(request, template_name, {'form':form})

def Doc_delete(request, pk, template_name='portal/Doc_delete.html'):
    removex = get_object_or_404(Document, pk=pk)
    if request.method=='POST':
        removex.delete()
        return redirect('profile')
    return render(request, template_name, {'object':removex})

# def Doc_reset(request,pk,template_name='portal/Doc_reset.html'):
#     resetx= get_object_or_404(Document, pk=pk)
#     form = ResetForm(request.POST or None, instance=resetx)
#     if form.is_valid():
#         form.save()
#         return redirect('profile')
#     return render(request, template_name, {'form'})



















