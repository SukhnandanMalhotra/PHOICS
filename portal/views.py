
from django.contrib.auth import login
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from phoics.settings import EMAIL_HOST_USER
from .tokens import account_activation_token
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from .models import Document, Profile
from .forms import DocumentForm, SignUpPage, Info, UpdateForm
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import ModelForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponse
"""
 it will work when user is logged in
 it will redirect to the user on login page 
 having next parameter default have SETTING.LOGIN_URL
"""


@login_required
def home(request):
    documents = Document.objects.order_by('-uploaded_at')
    profile_pic = Profile.objects.all
    return render(request,'portal/profile.html', {'documents': documents, 'profile_pic': profile_pic, })


# front page function which return front page html
def front_page(request):
    return render(request,'portal/front_page.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpPage(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            User.objects.filter(email=email).count()
            # if count is greater than zero it means this email id already exist
            if email and User.objects.filter(email=email).count() > 0:
                messages.error(request, 'this email-id already register', extra_tags='alert')
            else:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                # get_current_site used to get the url of current page
                current_site = get_current_site(request)
                subject = 'Activate Your phoics Account'
                # subject with email is send
                message = render_to_string('portal/account_activation_email.html', {
                    """
                    uid a user id encoded in base 64
                    token with uid make a unique link for every user 
                    user use to get user form information
                    
                    """
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                from_mail = EMAIL_HOST_USER
                to_mail = [user.email]
                # fail_silently false than it will raise as smtplib.SMTPException.
                send_mail(subject, message, from_mail, to_mail, fail_silently=False)

                messages.success(request, 'your email is successfully send')
                # return redirect('account_activation_sent')
    else:
        form = SignUpPage()
    return render(request, 'portal/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        # decode the uid from 64 base to normal text
        uid = force_text(urlsafe_base64_decode(uidb64))
        # fetch user information
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('profile')
    else:
        return render(request, 'portal/account_activation_invalid.html')


def newsfeed(request):
    documents = Document.objects.order_by('-uploaded_at')
    image=[]
    for obj in documents:
        if obj.status == "PUBLIC":
            image.append(obj)
    paginator = Paginator(image, 5)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
    return render(request,'portal/newsfeed.html', {'images': images})


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
        'form': form, 'title': 'Upload Image'
    })


def user_info(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    if request.method == 'POST':
        form = Info(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'your information saved successfully')
            return redirect('profile')
    else:
        form = Info()
    return render(request, 'portal/info.html', {'form': form})


def doc_update(request, pk, template_name='portal/model_form_upload.html'):
    updatex = get_object_or_404(Document, pk=pk)
    form = UpdateForm(request.POST or None, instance=updatex)
    if form.is_valid():
        form.save()
        return redirect('profile')
    return render(request, template_name, {'form':form, 'title': 'Edit Image'})


def doc_delete(request, pk):
    removex = get_object_or_404(Document, pk=pk)
    removex.delete()
    return redirect('profile')





# def Doc_reset(request,pk,template_name='portal/Doc_reset.html'):
#     resetx= get_object_or_404(Document, pk=pk)
#     form = ResetForm(request.POST or None, instance=resetx)
#     if form.is_valid():
#         form.save()
#         return redirect('profile')
#     return render(request, template_name, {'form':form})


def error_page(request):
    return render(request, 'portal/error_404.html')
