from django.shortcuts import render, redirect

from .models import Document
from .forms import DocumentForm

def home(request):
    documents = Document.objects.all()
    # profilepic=ProfilePic.objects.all()posts=Comment.objects.all()
    return render(request, 'portal/profile.html', {'documents': documents})


def newsfeed(request):
    documents = Document.objects.order_by('-uploaded_at')
    paginator = Paginator(documents, 20)
    page = request.GET.get('page')
    try:
        documents = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        documents = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        documents = paginator.page(paginator.num_pages)
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
