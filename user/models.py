from book.models import Book
from django.contrib.auth.models import User
from PIL import Image
from django.db import models



class Collection(models.Model):
    name                        =           models.CharField(max_length=50,)
    user                        =           models.ForeignKey(User,on_delete=models.CASCADE)
    books                       =           models.ManyToManyField(Book,related_name="coll")
    def __str__(self):
        return self.name


class Status(models.Model):
    STATUS                      =           (('NR', 'Not Read'), ('R', 'Read'), ('RG', 'Currently Reading'), ('TR', 'Want To Read'))
    read_status                 =           models.CharField(max_length=4,default='NR', choices=STATUS)
    page                        =           models.IntegerField(default=0)
    user                        =           models.ForeignKey(User,on_delete=models.CASCADE)
    book                        =           models.ForeignKey(Book,on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default ='default.png',upload_to = 'profile_pics')
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self,*args,**kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)