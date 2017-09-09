from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpPage


def home_page(request):
    return render(request,'polls/starting.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignUpPage(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            para = authenticate(username=username,password=raw_password)
            login(request,para)
            return redirect('starting')
    else:
        form = SignUpPage()
    return render(request,'polls/signup.html',{'form':form})
