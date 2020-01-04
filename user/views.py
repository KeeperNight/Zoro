from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from book.models import Book
from django.db.models import Q
from .models import Collection


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Your Account has been created successfully!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request,'user/registration.html',{'form':form})

def login(request):
    return render(request,'user/login.html',{'form':form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your Account has been updated successfully!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request,'user/profile.html',context)

def logout(request):
    return render(request,'user/main.html')

def home(request):
    return render(request,'user/main.html')

def about(request):
    return render(request,'user/about.html')
