from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request,'user/author_home.html')

def author_add_book(request):
    return render(request,'author/add_book.html')

def author_login(request):
    return render(request,'user/user_login.html')

def author_signup(request):
    return render(request,'user/user_signup.html')
