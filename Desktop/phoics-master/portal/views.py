from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .models import Document
from .forms import DocumentForm


def home(request):
     documents = Document.objects.all()
     return render(request,'portal/home.html', { 'documents': documents })


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'portal/model_form_upload.html', {
        'form': form
    })
