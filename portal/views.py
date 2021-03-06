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
from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Document, Profile, Comments
from .forms import DocumentForm, SignUpPage, Info, UpdateForm, SearchUser
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.contrib.auth.views import login
# from django.core import serializers
import json
from django.http import JsonResponse


# from django.shortcuts import (render_to_response)
# from django.template import RequestContext
#
#
# from django.core.files.storage import FileSystemStorage
# from django.conf import settings
from django.http import HttpResponse
"""
 it will work when user is logged out
 it will redirect to the user on login page 
 having next parameter default have SETTING.LOGIN_URL
"""


@login_required
def home(request, username):
    names2=[]
    form1 = DocumentForm(request.POST, request.FILES)
    if username == request.user.username:
        if request.method == 'POST':

            if form1.is_valid():
                upload_details = form1.save(commit=False)
                upload_details.user = request.user
                upload_details.save()
                return redirect(reverse('profile', kwargs={'username': username}))
        else:
            form1 = DocumentForm()
    # in order_by minus sign represent descending order
    form = SearchUser(request.POST)
    # user = User.objects.get(username=username)
    if form.is_valid():
        name = form.cleaned_data['username']
        names1 = User.objects.all()
        names2 = names1.filter(username__icontains=str(name))
    user = User.objects.get(username=username)
    user_image_count = user.document_set.all().count()
    documents = Document.objects.order_by('-uploaded_at')
    profile_pic = Profile.objects.filter(user=User.objects.get(username=username))
    print(profile_pic)
    return render(request, 'portal/profile.html',
                  {'documents': documents,
                   'profile_pic': profile_pic,
                   'username': username,
                   'user_image_count': user_image_count,'form':form1})



def check_login(request):
    if request.user.is_authenticated:
        return redirect('newsfeed')

    return login(request, template_name='portal/login.html')



def front_page(request):
    return render(request, 'portal/front_page.html')



def signup(request):
    if request.user.is_authenticated:
        return redirect('newsfeed')
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
                return render(request, 'portal/email_sent.html')

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


# def comment(request,pk):
#     global form1
#     image = Document.objects.get(pk=pk)
#     if request.method == 'POST':
#         form1 = CommentForm(request.POST)
#         if form1.is_valid():
#             form1.user = request.user
#             form1.document = image.document
#             form1.save()
#     return render(request,'portal/newsfeed.html', {'form1':form1})
#

@login_required
def newsfeed(request):
    documents = Document.objects.order_by('-uploaded_at')
    user = User.objects.get(username=request.user.username)
    comments = Comments.objects.order_by('-uploaded_at')
    profile = Profile.objects.all()
    image = []
    for obj in documents:
        if obj.status == "PUBLIC":
            image.append(obj)
    # now image object contain all the public images of user
    paginator = Paginator(image, 5)
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

    return render(request, 'portal/newsfeed.html', {'images': images,
                                                    'comments': comments,
                                                    'page_range': page_range,
                                                    'profile': profile,
                                                    # 'form': form, 'names': names2,
                                                    'user': user})


def comment(request):
    img_id = 0
    if request.method == 'GET':
        img_id=request.GET['imgid']

    if img_id:
        d = dict()
        image = Document.objects.get(pk=img_id)
        user = User.objects.get(username=str(request.user))
        com = request.GET['comment']
        d['user'] = user.username
        d['comment'] = com
        comm = Comments.objects.create(user=request.user, document=image, comment=com)
        x = json.dumps(d)
        return HttpResponse(x)


def model_form_upload(request, username):
    if username == request.user.username:
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                upload_details = form.save(commit=False)
                upload_details.user = request.user
                upload_details.save()
                return redirect(reverse('profile', kwargs={'username': username}))
        else:
            form = DocumentForm()
        return render(request, 'portal/profile.html', {
            'form': form,
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


def doc_update(request, username, pk, template_name='portal/edit_image.html'):
    if username == request.user.username:
        updatex = get_object_or_404(Document, pk=pk)
        form = UpdateForm(request.POST or None, instance=updatex)
        if username == updatex.user.username:
            if form.is_valid():
                form.save()
                return redirect(reverse('profile', kwargs={'username': username}))
            else:
                print("---edit image form is not valid---")
            return render(request, template_name, {'form': form, 'title': 'Edit Image', 'updatex': updatex})
        else:
            print("---you are not correct user for edit image---")
    else:
        print("---edit image form is not working proper---")
    return redirect(reverse('profile', kwargs={'username': username}))

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



@login_required
def like(request):
    imgid = None
    if request.method == 'GET':
        data = dict()
        imgid = request.GET['imgid']
        img = Document.objects.get(id=int(imgid))
        print("-----we get id-----")
        if request.user in img.like_user.all():
            img.like_user.remove(request.user)
            img.like_or_not = 0
            img.save()
        else:
            img.like_user.add(request.user)
            img.like_or_not = 1
            img.save()
        a = img.like_user.count()
        x = img.like_user.all()
        us = User.objects.get(username=request.user.username)
        print(x)
        print(img.like_user)
        if us in x:
            print("yes")
        else:
            print("no")
        b = img.like_or_not
        data = {
            'count_like': a,
            'state_image': b
        }
        print(data)
        print(a)
        return JsonResponse(data)


def list_of_user(request):
    imgid = None
    if request.method == 'GET':
        imgid = request.GET['imgid']
        img = Document.objects.get(id=int(imgid))
        x = img.like_user.all()
        # y = ','.join(x)
        print(x)
        return HttpResponse(x)


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def validate_emailid(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)


def rotate_image(request):
    rotate = request.GET.get('rotate', None)
    imgid = request.GET.get('imgid')
    print(imgid)
    img = Document.objects.get(id=int(imgid))
    img.rotate = rotate
    img.save()
    print("rotate")
    data = {
        'img_source': str(img.document)
    }
    return JsonResponse(data)


def blur_image(request):
    blur = request.GET.get('blur', None)
    imgid = request.GET.get('imgid')
    print(imgid)
    img = Document.objects.get(id=int(imgid))
    img.blur = blur
    img.save()
    print("blur")
    data = {
        'img_source': str(img.document)
    }
    return JsonResponse(data)


def width_image(request):
    width = request.GET.get('width', None)
    imgid = request.GET.get('imgid')
    print(imgid)
    img = Document.objects.get(id=int(imgid))
    img.width = int(width)
    img.save()
    print("width")
    data = {
        'img_source': str(img.document)
    }
    return JsonResponse(data)


def height_image(request):
    height = request.GET.get('height', None)
    imgid = request.GET.get('imgid')
    print(imgid)
    img = Document.objects.get(id=int(imgid))
    img.height = int(height)
    img.save()
    print("height")
    data = {
        'img_source': str(img.document)
    }
    return JsonResponse(data)


def flip_image(request):
    flip = request.GET.get('flip', None)

    imgid = request.GET.get('imgid')
    img = Document.objects.get(id=int(imgid))
    img.flip = flip
    img.save()
    data = {
        'img_source': str(img.document)
    }
    return JsonResponse(data)


def effect_image(request):
    effect = request.GET.get('effect')
    imgid = request.GET.get('imgid')
    img = Document.objects.get(id=int(imgid))
    img.effect = int(effect)
    img.save()
    data = {
        'img_source': str(img.document)
    }
    print("kya hua be")
    return JsonResponse(data)


def search(request):
    search_user1 = dict()
    search_data = request.GET.get('search_data')
    all_user = User.objects.all()
    search_user = all_user.filter(username__icontains=str(search_data))
    print("-----", search_user)
    for i in range(search_user.count()):
        print(search_user[i])
        search_user1[str(search_user[i])] = str(search_user[i])
    print(search_user1)
    return JsonResponse(search_user1)

