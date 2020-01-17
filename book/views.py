from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Book,Genre,Chapter
from django.contrib.auth.mixins import LoginRequiredMixin
from author.models import Author
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
# from user.models import Read
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user.models import Collection,Status

def about_book(request):
    return render(request, 'book/book.html')

def home(request):
    query_list = Book.objects.all()
    collections=Collection.objects.filter(user=request.user.id)
    status = Status.objects.filter(user=request.user.id)
    print(status)
    print(collections)
    query = request.GET.get("q")
    new_coll = request.GET.get('coll')
    if new_coll:
        Collection.objects.create(name=new_coll,user_id=request.user.id)
    if query:
        query_list= query_list.filter(
            Q(name__icontains=query)|
            Q(author__name__icontains=query)|
            Q(genre__genre__icontains=query)
            ).distinct()
    paginator =Paginator(query_list,12)
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
        "page_request_var":page_request_var,
        "collections":collections,
        "status":status
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


class ChapterDetailView(DetailView):
    model = Chapter


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    fields = ['name', 'genre', 'published_date', 'image','author']

    def form_valid(self, form):
        form.instance.book_creator = self.request.user
        return super().form_valid(form)

class ChapterCreateView(LoginRequiredMixin, CreateView):
    model = Chapter
    fields = ['book', 'name', 'content']

    def form_valid(self, form):
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ['name', 'genre','image','author','published_added']

    def form_valid(self, form):
        form.instance.book_creator = self.request.user
        form.save()
        return super().form_valid(form)


class ChapterUpdateView(LoginRequiredMixin, UpdateView):
    model = Chapter
    fields = ['book', 'name', 'content']

    def form_valid(self, form):
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


@login_required
def add_collection(request,book_id,collection_id):
    book=get_object_or_404(Book,id=book_id)
    collection=get_object_or_404(Collection,id=collection_id)
    if collection.books.filter(id=book.id).exists():
        collection.books.remove(book)
    else:
        collection.books.add(book)
    return HttpResponseRedirect(book.get_absolute_url())


@login_required
def collection(request):
    collections=Collection.objects.filter(user=request.user.id)
    context={
        "collections":collections,
    }
    return render(request,'book/collection.html',context)

@login_required
def books_in_collection(request,collection_id):
    coll=get_object_or_404(Collection,id=collection_id)
    collections=Collection.objects.filter(user=request.user.id)
    collection_count=coll.books.count()
    books = coll.books.all()
    query = request.GET.get("q")
    new_coll = request.GET.get('coll')
    if new_coll:
        Collection.objects.create(name=new_coll,user_id=request.user.id)
    if query:
        books= books.filter(
            Q(name__icontains=query)|
            Q(author__name__icontains=query)|
            Q(genre__genre__icontains=query)
            ).distinct()
    paginator =Paginator(books,10)
    page_request_var="page"
    page=request.GET.get(page_request_var)
    try:
        query=paginator.get_page(page)
    except PageNotAnInteger:
        query=paginator.get_page(1)
    except EmptyPage:
        query=paginator.get_page(paginator.num_pages)
    print("completed packing")
    context={
        "books":query,
        "page_request_var":page_request_var,
        "collections":collections,
        'collection_name':coll.name,
        'collection_count':collection_count,
        'message':'Search your collection '
    }
    return render(request, "book/home.html", context=context)

@login_required
def add_status(request,book_id,stat_id):
    book=get_object_or_404(Book,id=book_id)
    stat=get_object_or_404(Status,id=stat_id)
    if stat.book.get(id=book.id).exists():
        stat.book.remove(book)
    else:
        stat.book.add(book)
    return HttpResponseRedirect(book.get_absolute_url())
