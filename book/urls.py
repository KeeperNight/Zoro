from django.urls import path,include
from .views import BookCreateView, BookDetailView, BookUpdateView, AuthorBookListView, GenreBookListView
from . import views


urlpatterns = [
    path('book_list/',views.home, name="home"),
    path('author/<str:username>', AuthorBookListView.as_view(), name="author-book"),
    path('genre/<str:genrename>', GenreBookListView.as_view(), name="genre-book"),
    path('book/<int:pk>/', BookDetailView.as_view(), name="book-detail"),
    path('book/<int:pk>/update/', BookUpdateView.as_view(), name="book-update"),
    path('new/', BookCreateView.as_view(), name="book-create"),
    path('<book_id>/add_favorite/',views.add_favorite, name='favorite'),
    path('genre/',views.genre, name="genre"),
    path('favorite/',views.favorite, name="favorites"),
    path('ratings/', include('star_ratings.urls', namespace='ratings'))
]
