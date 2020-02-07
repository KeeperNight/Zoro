from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from book.models import Book
from django.db.models import Q
from .models import Collection,Profile
from django.contrib.auth.models import User
from friendship.models import Friend, Follow, Block
from book.models import Book
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import profileSerializer
from django.shortcuts import render_to_response
from django.template import RequestContext


#Home Page
def home(request):
    #Querying required data
    query_list = Book.objects.all()
    collections=Collection.objects.filter(user=request.user.id)

    #Evaluating Qurey from FORM
    query = request.GET.get("q")
    new_coll = request.GET.get('coll')
    #Checking if collection is new and creating it if it's new
    if new_coll:
        Collection.objects.create(name=new_coll,user_id=request.user.id)
    user_list=[]
    #Filtering out required data
    if query:
        query_list= query_list.filter(
            Q(name__icontains=query)|
            Q(genre__genre__icontains=query)
        ).distinct()
        #Searching Users by their username, firstname and lastname
        user_list = User.objects.filter(
            Q(username__icontains = query)|
            Q(first_name__icontains = query)|
            Q(last_name__icontains=query)
        ).distinct()

    #Paginating books result
    paginator =Paginator(query_list,10)
    page_request_var="page"
    page=request.GET.get(page_request_var)
    try:
        queryset=paginator.get_page(page)
    except PageNotAnInteger:
        queryset=paginator.get_page(1)
    except EmptyPage:
        queryset=paginator.get_page(paginator.num_pages)

    #Paginating users result
    paginator_user =Paginator(user_list,5)
    page_request_var="page"
    page=request.GET.get(page_request_var)
    #Packing result into users list
    try:
        users=paginator_user.get_page(page)
    except PageNotAnInteger:
        users=paginator_user.get_page(1)
    except EmptyPage:
        users=paginator_user.get_page(paginator_user.num_pages)

    #Sending data to page
    context={
        "books":queryset,
        "page_request_var":page_request_var,
        "collections":collections,
        "users":users,
    }
    #returns home page in books
    return render(request, 'user/home.html', context)


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

def main(request):
    return render(request,'user/main.html')

def about(request):
    return render(request,'user/about.html')

def view_user_profile(request,user_id):
    return render(request, 'user/profile.html')

def friends(request):
    return render(request, 'user/friends.html')

class profileList(APIView):
    def get(self,request):
        profile1=User.objects.all()
        serializer=profileSerializer(profile1, many=True)
        return Response(serializer.data)
        
    def post(self):
        pass


def handler404(request, exception):
    response = render_to_response("user/404.html")
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('user/500.html')
    response.status_code = 500
    return response