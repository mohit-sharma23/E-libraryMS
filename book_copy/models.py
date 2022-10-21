from django.db import models
import os

# Create your models here.


class Book(models.Model):
    btitle = models.TextField(max_length=30)
    bauthor = models.TextField(max_length=30)
    bgenre = models.TextField(max_length=30)
    bpreface = models.TextField()
    bfile = models.FileField(default='download.jpg', upload_to='static/')

    def __str__(self):
        return self.btitle
