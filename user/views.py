from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from book.models import Book
from django.db.models import Q
from .models import Collection
from django.contrib.auth.models import User
from friendship.models import Friend, Follow, Block


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

def view_user_profile(request,user_id):
    return render(request, 'user/profile.html')

def friends(request):
    all_friends = Friend.objects.friends(request.user)
    return render(request,'user/friends.html',{'friends':friends})

def unread_request(request):
    requests = Friend.objects.unread_requests(user=request.user)
    context={
        'requests':requests
    }
    return render(request,'user/unread.html', context)

def reject(request):
    rejects = Friend.objects.rejected_requests(user=request.user)
    context={
        'rejects':rejects
    }
    return render(request,'user/reject.html', context)    

def reject(request):
    all_followers = Following.objects.followers(request.user)
    context={
        'all_followers':all_followers
    }
    return render(request,'user/followers.html', context) 

def reject(request):
    following = Following.objects.following(request.user)
    context={
        'following':following
    }
    return render(request,'user/following.html', context)     


