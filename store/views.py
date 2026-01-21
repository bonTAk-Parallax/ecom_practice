from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import NewUserForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

# Create your views here.


def register_request(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration Successful.")
            return HttpResponse("Congratulation!")
        messages.error(request, "Could not register!")
    form = NewUserForm()
    return render(request=request, template_name="store/register.html", context={'register_form': form})


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return HttpResponse("Logged In!!!")
            else:
                messages.error(request, "Invalid username or password!")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request, "store/login.html", {'login_form': form})

