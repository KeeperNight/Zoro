from django.db import models
from django.urls import reverse
from author.models import Author
from django.contrib.auth.models import User
from PIL import Image
from datetime import date
from django.core.files.storage import FileSystemStorage
from .validators import validate_file_extension
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager


class Genre(models.Model):
    genre                       =           models.CharField(max_length=30,default="not set")
    def __str__(self):
        return self.genre


class Book(models.Model):
    name                        =           models.CharField(max_length=200)
    rating                      =           models.PositiveIntegerField(default=0)
    PUBLISHED                   =           (('D', 'Draft'), ('P', 'Published'))
    image                       =           models.ImageField(default='default.jpg', upload_to='book_covers')
    published                   =           models.CharField(max_length=2, choices=PUBLISHED)
    author                      =           models.ManyToManyField(Author, related_name="book_author")
    book_creator                =           models.ForeignKey(User, on_delete=models.CASCADE)
    date_added                  =           models.DateField(("Date"), auto_now_add=True)
    pages                       =           models.PositiveIntegerField(default=0)
    favorite                    =           models.ManyToManyField(User, related_name="favorite")
    genre                       =           models.ManyToManyField(Genre, related_name="book_genre")
    isbn13                      =           models.IntegerField(null=True)
    published_date              =           models.DateField(unique=False)
    start_date                  =           models.DateField(null=True)
    end_date                    =           models.DateField(null=True)
    tags                        =           TaggableManager()
    prog                        =           models.ManyToManyField(User,related_name='pro',through='Progress')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home')

    def save(self,*args,**kwargs):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 200 or img.width > 200:
            output_size = (150, 150)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Chapter(models.Model):
    name                        =           models.CharField(max_length=40)
    content                     =           RichTextUploadingField()
    book                        =           models.ForeignKey(Book, on_delete=models.CASCADE,related_name="chapters")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home')

class Progress(models.Model):
    STATUS = (('Read','Read'),('To-be-Read','To-be-Read'),('Now Reading','Now Reading'))
    prog = models.CharField(max_length=32,choices=STATUS)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)