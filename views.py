from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .models import Document
from .forms import DocumentForm


def home(request):
     documents = Document.objects.all()
     return render(request,'portal/profile.html', { 'documents': documents })


def newsfeed(request):
    documents = Document.objects.all()
    return render(request, 'portal/newsfeed.html', {'documents': documents})

# def profilepic(request):
#     if request.method == 'POST':
#         form = ProfileImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     else:
#         form = DocumentForm()
#     return render(request, 'portal/profilepic.html', {'form': form})

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
