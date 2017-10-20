from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from phoics.settings import EMAIL_HOST_USER
from .tokens import account_activation_token
from django.shortcuts import render, redirect, get_object_or_404, render_to_response,reverse
from .models import Document, Profile
from .forms import DocumentForm, SignUpPage, Info, UpdateForm
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import (render_to_response)
from django.template import RequestContext


from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponse
"""
 it will work when user is logged in
 it will redirect to the user on login page 
 having next parameter default have SETTING.LOGIN_URL
"""


@login_required
def home(request, username):
    # in order_by minus sign represent descending order

    documents = Document.objects.order_by('-uploaded_at')
    profile_pic = Profile.objects.all
    return render(request, 'portal/profile.html',
                  {'documents': documents,
                   'profile_pic': profile_pic,
                   'username': username})


# front page function which return front page html
def front_page(request):
    return render(request, 'portal/front_page.html')


def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(reverse('profile', kwargs={'username': username}))
    else:
        return render(request, 'portal/login.html')


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
                    uid contain user id encoded in base 64
                    token help to make link as it work only once
                    user use to get user form information
                    domain - 127.0.0.1:8000
                    """
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                from_mail = EMAIL_HOST_USER
                to_mail = [user.email]
                # fail_silently "false", then if error in sending email it will raise -
                # smtplib.SMTPException, SMTPServerDisconnected, SMTPDataError,etc.
                send_mail(subject, message, from_mail, to_mail, fail_silently=False)
                messages.success(request, 'your email is successfully send')

    else:
        form = SignUpPage()
    return render(request, 'portal/signup.html', {'form': form})


# when user click on email link then this function execute
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
        return redirect('newsfeed')
    else:
        return render(request, 'portal/account_activation_invalid.html')


@login_required
def newsfeed(request):
    documents = Document.objects.order_by('-uploaded_at')
    image = []
    for obj in documents:
        if obj.status == "PUBLIC":
            image.append(obj)
    # now image object contain all the public images of user
    paginator = Paginator(image, 2)
    # here 2 means one page contain two images
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # if page number is not an integer redirect to page no 1
        images = paginator.page(1)
    except EmptyPage:
        # if page has no images , redirect to last page
        images = paginator.page(paginator.num_pages)
    # this is for display pages no. near to current page
    current_page_no = images.number
    total_pages = len(paginator.page_range)
    before_show = current_page_no - 6 if current_page_no >= 6 else 0
    after_show = current_page_no + 6 if current_page_no <= total_pages - 6 else total_pages
    page_range = paginator.page_range[before_show:after_show]

    return render(request, 'portal/newsfeed.html', {'images': images, 'page_range': page_range})


def model_form_upload(request, username):
    if username == request.user.username:
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                width = form.cleaned_data.get('width')
                height = form.cleaned_data.get('height')
                upload_details = form.save(commit=False)
                upload_details.user = request.user
                upload_details.save()
                if width < 0 or height < 0:
                    messages.error(request, 'Enter valid width and height')
                    return redirect('model_form_upload')
                return redirect(reverse('profile', kwargs={'username': username}))
        else:
            form = DocumentForm()
        return render(request, 'portal/model_form_upload.html', {
            'form': form, 'title': 'Upload Image'
                  })


def user_info(request, username):
    if username == request.user.username:

        obj = Profile.objects.get(user=request.user)
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:            # if profile is not updated, save previous profile data
            profile = Profile(user=request.user)
        if request.method == 'POST':
            form = Info(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'your information saved successfully')
                return redirect(reverse('profile', kwargs={'username': username}))
        else:
            form = Info()
        return render(request, 'portal/info.html', {'form': form, 'obj': obj})


def doc_update(request, pk, username, template_name='portal/model_form_upload.html'):
    if username == request.user.username:
        updatex = get_object_or_404(Document, pk=pk)
        form = UpdateForm(request.POST or None, instance=updatex)
        if form.is_valid():
            form.save()
            return redirect(reverse('profile', kwargs={'username': username}))
        return render(request, template_name, {'form': form, 'title': 'Edit Image'})


# it will delete the selected image through 'delete()'
# def doc_delete(request, pk, template_name='portal/profile.html'):
#     removex = get_object_or_404(Document, id=pk)
#     if request.method == 'POST':
#         removex.delete()
#         return redirect('profile')
#     return render(request, template_name, {'object': removex})

def doc_delete(request, pk, username):
    removex = get_object_or_404(Document, id=pk)
    removex.delete()
    return HttpResponseRedirect(reverse('profile', args=(username,)))
    # return redirect('profile/' username)


def error404(request):
    return render(request, 'portal/error_404.html', {'name': '404', 'title': 'Page not found'})


def error400(request):
    return render(request, 'portal/error_404.html', {'name': '400', 'title': 'Bad Request'})


def error403(request):
    return render(request, 'portal/error_404.html', {'name': '403', 'title': 'Permission Denied'})


def error500(request):
    return render(request, 'portal/error_404.html', {'name': '500', 'title': 'Server Error'})
