"""
This is a doc string
"""
from django.contrib.auth import login
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from phoics.settings import EMAIL_HOST_USER
from .tokens import account_activation_token
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from .models import Document
from .forms import DocumentForm, SignUpPage
from django.contrib.auth.views import password_reset
#from .forms import ForgetPassword, OTPForm
from . import forms
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import random
from django.http import HttpResponse



"""
 it will work when user is logged in
 it will redirect to the user on login page 
 having next parameter default have SETTING.LOGIN_URL
"""
@login_required
def home(request):
    documents = Document.objects.order_by('-uploaded_at')
    return render(request,'portal/profile.html', {'documents': documents})


# front page function which return front page html
def front_page(request):
    return render(request,'portal/front_page.html')

"""
signup all functionality

"""
def signup(request):
    if request.method == 'POST':
        form = SignUpPage(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            User.objects.filter(email=email).count()
            # if count is greater than zero it means this email id already exist
            if email and User.objects.filter(email=email).count() > 0:
                raise ValidationError('this email user already exist')
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
                    token with uid make a unque link for every user 
                    user use to get user form information
                    
                    """
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                from_mail=EMAIL_HOST_USER
                to_mail=[user.email]
                # fail_silently false than it will raise as smtplib.SMTPException.
                send_mail(subject, message,from_mail,to_mail,fail_silently=False)
                return redirect('account_activation_sent')
    else:
        form = SignUpPage()
    return render(request, 'portal/signup.html', {'form': form})

def account_activation_sent(request):
    return render(request, 'portal/account_activation_sent.html')

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
    return render(request,'portal/newsfeed.html', {'documents': documents})

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

"""
this is that code that we want to follow for forget password before now code
"""
# def forget_pass(request):
#     if request.method == 'POST':
#         form = ForgetPassword(request.POST)
#         if form.is_valid():
#             your_email = form.cleaned_data.get('your_email')
#             subject = 'reset your password'
#             message = render_to_string('portal/forget_email_sent.html', {
#                   })
#             from_mail = EMAIL_HOST_USER
#             to_mail = [your_email]
#             send_mail(subject, message, from_mail, to_mail, fail_silently=False)
#             return redirect('enter_otp')
#
#     else:
#         form = ForgetPassword()
#     return render(request, 'portal/forget_page.html', {'form': form})

# def enter_otp(request):
#     if request.method == 'POST':
#         form = OTPForm(request.POST)
#         if form.is_valid():
#             your_otp = form.cleaned_data.get('otp')
#             return redirect('reset_password')
#     else:
#         form = OTPForm()
#     return render(request, 'portal/enter_otp.html', {'form':form})
#
# def reset_pass(request):
#     if request.method == 'POST':
#         form = YourNewPassword(request.POST)
#         if form.is_valid():
#             your_user_name = form.cleaned_data.get('your_user_name')
#             old_password = form.cleaned_data.get('old_password')
#             new_password = form.cleaned_data.get('new_password')
#             user_exist = User.objects.filter(Q(username=your_user_name) and Q(password=old_password))
#             if user_exist.exists():
#                 user_exist.password = new_password
#                 return redirect('front_page')
#             else:
#                 return HttpResponse('user does not exist')
#
#     else:
#         form = YourNewPassword()
#     return render(request, 'portal/reset_password_form.html', {'form': form})
#
