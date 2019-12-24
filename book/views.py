from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Book,Genre
from django.contrib.auth.mixins import LoginRequiredMixin
from author.models import Author
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
# from user.models import Read
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def about_book(request):
    return render(request, 'book/book.html')

def home(request):
    query_list = Book.objects.all()
    query = request.GET.get("q")
    if query:
        query_list= query_list.filter(
            Q(name__icontains=query)|
            Q(author__name__icontains=query)|
            Q(genre__genre__icontains=query)
            ).distinct()
    paginator =Paginator(query_list,10)
    page_request_var="page"
    page=request.GET.get(page_request_var)
    try:
        queryset=paginator.get_page(page)
    except PageNotAnInteger:
        queryset=paginator.get_page(1)
    except EmptyPage:
        queryset=paginator.get_page(paginator.num_pages)  
    context={
        "books":queryset,
        "page_request_var":page_request_var
    }
    #returns home page in books
    return render(request, 'book/home.html', context)

#Genre function to retrieve genres
def genre(request):
    query_list = Genre.objects.all()
    query = request.GET.get("q")
    if query:
        query_list= query_list.filter(
            Q(genre__icontains=query)
            ).distinct()
        print(query_list)
    context={
        "genres":query_list,
    }
    return render(request,'book/genre.html', context)


#Shows detail view of book
class BookDetailView(DetailView):
    model = Book



# def book(request,pk):
    # user = request.user
    # book = User.objects.filter(id=pk)
    # print(book)
    # is_favorite = False
    # if book:
    #     is_favorite=True
    # context = {'book': book,"is_favorite":is_favorite}
    # return render(request, "book/book_detail.html", context=context)


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    fields = ['name', 'genre', 'published', 'image','author','date_added']

    def form_valid(self, form):
        form.instance.book_creator = self.request.user
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ['name', 'genre', 'published', 'image','author','date_added']

    def form_valid(self, form):
        form.instance.book_creator = self.request.user
        form.save()
        return super().form_valid(form)



class AuthorBookListView(ListView):
    model = Book
    template_name = 'book/author_books.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'books'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(Author, name=self.kwargs.get('username'))
        return Book.objects.filter(author=user)


class GenreBookListView(ListView):
    model = Book
    template_name = 'book/genre_books.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'books'
    paginate_by = 5

    def get_queryset(self):
        genre = get_object_or_404(Genre, genre=self.kwargs.get('genrename'))
        print(genre)
        return Book.objects.filter(genre=genre)

@login_required 
def favorite(request):
    user = request.user
    books = user.favorite.all()
    context = {'books': books}
    return render(request, "book/favorite.html", context=context)

@login_required
def add_favorite(request,book_id):
    book=get_object_or_404(Book,id=book_id)
    if book.favorite.filter(id=request.user.id).exists():
        book.favorite.remove(request.user)
    else:
        book.favorite.add(request.user)
    return HttpResponseRedirect(book.get_absolute_url())