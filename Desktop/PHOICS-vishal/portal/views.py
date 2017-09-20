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
from .forms import SignUpPage, forget_password
from .tokens import account_activation_token
from django.shortcuts import render, redirect

from .models import Document
from .forms import DocumentForm

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

def signup(request):
    if request.method == 'POST':
        form = SignUpPage(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            User.objects.filter(email=email).count()
            if email and User.objects.filter(email=email).count() > 0:
                raise ValidationError('this email user already exist')
            else:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                # get_current_site used to get the url of current page
                current_site = get_current_site(request)
                subject = 'Activate Your phoics Account'
                message = render_to_string('portal/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                from_mail=EMAIL_HOST_USER
                to_mail=[user.email]
                send_mail(subject, message,from_mail,to_mail,fail_silently=False)
                return redirect('account_activation_sent')
    else:
        form = SignUpPage()
    return render(request, 'portal/signup.html', {'form': form})

def account_activation_sent(request):
    return render(request, 'portal/account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('')
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

def forget_pass(request):
    if request.method == 'POST':
        form = forget_password(request.POST)
        if form.is_valid():
            form.save(commit=False)
            your_email = form.cleaned_data.get('your_email')
            return redirect('front_page')

    else:
        form = forget_password()
    return render(request, 'portal/forget_page.html',{'form':form})
