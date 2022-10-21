
from django.contrib import admin
from django.urls import path,include
from .views import *
# from accounts import views


urlpatterns = [
   # path('register/',views.register),
   # path('admin/', admin.site.urls),
   # path('about-us/',views.aboutUs),
   #path('',views.home),
   #path('login/',views.login),
   path('priyanshu/',account, name="account"),
   path('forget-password/' , ForgetPassword, name="forget-password"),
   path('change-password/<token>/' , ChangePassword , name="change_password"),


]