from django.urls import path,include
from .views import BookCreateView, ChapterCreateView, BookDetailView, ChapterDetailView, BookUpdateView, ChapterUpdateView, AuthorBookListView, GenreBookListView
from . import views


urlpatterns = [
    path('',views.home, name="home"),
    path('author/<str:username>', AuthorBookListView.as_view(), name="author-book"),
    path('genre/<str:genrename>', GenreBookListView.as_view(), name="genre-book"),
    path('<int:pk>/', BookDetailView.as_view(), name="book-detail"),
    path('chapter/<int:pk>/', ChapterDetailView.as_view(), name="chapter-detail"),
    path('book/<int:pk>/update/', BookUpdateView.as_view(), name="book-update"),
    path('chapter/<int:pk>/update/', ChapterUpdateView.as_view(), name="chapter-update"),
    path('new/', BookCreateView.as_view(), name="book-create"),
    path('newchapter/', ChapterCreateView.as_view(), name="chapter-create"),
    path('<book_id>/add_favorite/',views.add_favorite, name='favorite'),
    path('genre/',views.genre, name="genre"),
    path('favorite/',views.favorite, name="favorites"),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('collection/', views.collection, name='collection'),
    path('<collection_id>/books_in_collection/', views.books_in_collection, name='books_in_collection'),
    path('<collection_id>/<book_id>/add_collection/',views.add_collection, name='add_collection'),
    path('<stat_id>/<book_id>/add_status/',views.add_status, name='add_status'),
    path('articles/comments/', include('django_comments.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
