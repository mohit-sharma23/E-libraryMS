from django.contrib import admin
from .models import Post, Profilepic
from django.contrib.auth.models import User
admin.site.register(Post)
admin.site.register(Profilepic)

# Register your models here.
