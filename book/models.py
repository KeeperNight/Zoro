from django.db import models
from django.urls import reverse
from author.models import Author
from django.contrib.auth.models import User
from PIL import Image


class Genre(models.Model):
    genre                 =           models.CharField(max_length=30,default="not set")
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
    date_added                  =           models.DateField()
    pages                       =           models.PositiveIntegerField(default=0)
    favorite                    =           models.ManyToManyField(User, related_name="favorite")
    genre                       =           models.ManyToManyField(Genre, related_name="book_genre")
    read                        =           models.ManyToManyField(User, related_name="book_read")
    isbn                        =           models.IntegerField(null=True)
    published_date              =           models.DateField()

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

class Comment(models.Model):
    user                        =           models.ForeignKey(User,on_delete=models.CASCADE)
    book                        =           models.ForeignKey(Book,on_delete=models.CASCADE)
    STATUS                      =           (('C','Completed'),('R','Reading...'),('CC','Yet to complete'),('NS','Not Started'))
    status                      =           models.CharField(choices=STATUS,max_length=3)