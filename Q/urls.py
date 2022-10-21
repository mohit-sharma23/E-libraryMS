
from django.contrib import admin
from django.contrib.auth import views as auth_views
from Q import views, tokens
from book_copy import views as views1
from django.urls import path, include
# from Book.views import views as BookView
# from Book.views import CreateCheckOutSessionView
urlpatterns = [
    path('admin', admin.site.urls),
    # path('create-checkout-session', CreateCheckOutSessionView.as_view(),
    #      name='create-checkout-session'),
    path('register/', views.register, name="register"),
    path('signout/', auth_views.LogoutView.as_view(), name="signout"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/index_R.html'), name='loginapp'),
    path('upload/', views1.form, name='form'),
    path('profile/', views1.profile, name='profile'),
    path('yourbooks/', views1.uploads, name='Uploads'),
    path('', include('accounts.urls')),
    path('login/', views.login, name="login"),
    path('', include('Book.urls')),
]
