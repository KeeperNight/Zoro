from django.db import models


class Author(models.Model):
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return str(self.name)
