from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from PIL import Image


class Post(models.Model):
    Book_name = models.CharField(max_length=50)
    Author = models.CharField(max_length=50)
    date_uploaded = models.DateTimeField(default=timezone.now)
    Info = models.CharField(max_length=1000)
    Genre = models.CharField(max_length=30)
    HPrice = models.IntegerField(default=0)
    SPrice = models.IntegerField(default=0)
    Uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    Image = models.ImageField(default='default.jpg', upload_to='media/images')
    File = models.FileField(default='default.pdf', upload_to='media/files')
    Language = models.CharField(default='null', max_length=50)
    # PublishedIn = models.DateField(default=datetime.date.today)
    PublishedIn = models.DateTimeField(default=timezone.now)
    upvotes = models.ManyToManyField(User, related_name='upv')
    downloads = models.ManyToManyField(User, related_name='down')
    reads = models.ManyToManyField(User, related_name='reads')
    buy = models.ManyToManyField(User, related_name='buy')
    fav = models.ManyToManyField(User, related_name='fav')


class Profilepic(models.Model):
    userp = models.ForeignKey(User, on_delete=models.CASCADE)
    about = models.TextField(default=" ", max_length=50)
    Image = models.ImageField(default='default.jpg', upload_to='media/images')

    def __str__(self):
        return self.userp.username
