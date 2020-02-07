from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from user import views


urlpatterns = [
    path('', views.main,name="main"),
    path('zoro/',views.home, name="home"),
    path('profile/', views.profile, name='profile'),
    path('about/',views.about,name="about"),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('messages/', include('postman.urls', namespace='postman'), name='messages'),
    path('password-reset/',
    	auth_views.PasswordResetView.as_view(
             template_name='user/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='user/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='user/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='user/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('friendship/', include('friendship.urls')),
    path('friends/',views.friends, name="friend"),
    path('tellme/', include("tellme.urls")),
    path('user_api/',views.profileList.as_view()),
]

