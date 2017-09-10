from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpPage
from django.contrib.auth.decorators import login_required


@login_required
# function that call html file where user enter after signup and login
def home_page(request):
    return render(request,'portal/home.html')


# all working of signup start from here
def sign_up(request):
    if request.method == 'POST':
        form = SignUpPage(request.POST)

        # checking form fillup by them is correct or not ...
        if form.is_valid():
            # ..if correct it will execute
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # authenticate give boolean expression like yes or none
            para = authenticate(username=username,password=raw_password)
            # if para is not none this login the user and reach on home page
            login(request,para)
            # it is a direct process for both login and logout
            return redirect('home')

    else:
        # method is not post it call signuppage() function without passing arguments
        form = SignUpPage()
        # now we reach on sign up html page
    return render(request,'portal/signup.html',{'form':form})


