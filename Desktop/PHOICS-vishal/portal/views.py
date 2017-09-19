from django.shortcuts import render, redirect

from .models import Document,Comment
from .forms import DocumentForm

def home(request):
    documents = Document.objects.all()
    # profilepic=ProfilePic.objects.all()
    posts=Comment.objects.all()
    return render(request, 'portal/profile.html', {'documents': documents,'post':posts})


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
#         form = ProfileImageForm()
#     return render(request, 'portal/model_form_upload.html', {'form': form})

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            profile1 = form.save(commit=False)
            profile1.user = request.user
            profile1.save()
            return redirect('profile')
    else:
        form = DocumentForm()
    return render(request, 'portal/model_form_upload.html', {
        'form': form
    })
