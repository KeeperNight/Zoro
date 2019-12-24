from django.urls import path

from . import views

urlpatterns=[
    path('',views.home,name="author"),
    path('login/',views.author_login,name='author_login'),
    path('signup/',views.author_signup,name='author_signup'),
    path('add_book/',views.author_add_book,name="author_add_book")
]
