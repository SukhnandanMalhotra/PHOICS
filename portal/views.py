from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from .forms import SignUpPage
from .tokens import account_activation_token
@login_required
# function that call html file where user enter after signup and login
def home_page(request):
    return render(request,'portal/home.html')


# all working of signup start from here
def sign_up(request):
    if request.method == 'POST':
        form = SignUpPage(request.POST)

        # checking form fill up by them is correct or not ...
        if form.is_valid():
            # ..if correct it will execute
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            #  authenticate give boolean expression like yes or none
            # para = authenticate(username=username,password=raw_password)

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('portal/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

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
        return redirect('home')
    else:
        return render(request, 'portal/account_activation_invalid.html')
