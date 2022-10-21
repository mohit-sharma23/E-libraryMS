
from email import message
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from Q import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from django.core.mail import EmailMessage, send_mail
from accounts .models import *


def home(request):
    data = {
        'title': 'home page',
        'hello': 'My new website',
        'student_details': [{'name': 'pradip', 'phone': 9258645545},
                            {'name': 'ram', 'phone': 9258645985}]
    }
    return render(request, "accounts/index.html", data)


def register(request):
    print("dndj")
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username):
            messages.error(
                request, "Username already exist! please try some other username ")
            return redirect('/login')
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered! ")
            return redirect('/login')

        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('login')
        if password1 != password2:
            messages.error(request, "Passwords didnt match!")
            return redirect('/login')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha_Numeric!")
            return redirect('/login')

        myuser = User.objects.create_user(username, email, password1)
        myuser.first_name = first_name
        myuser.is_active = False

        myuser.save()
        messages.success(
            request, "Check for Verification Email on your registered Email Address..")
        profile_obj = Profile.objects.create(user=myuser)
        print(profile_obj)
        profile_obj.save()

        # Welcome Email

        subject = "Welcome to Bookalicious Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + \
            "Welcome to Bookalicious!! \n Thank you for Visiting our website \n we have also sent confirmation email,please confirm your email address in order to activate your account. \n \n Thanking You\n Bookalicious Team "
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # confirmation mail
        current_site = get_current_site(request)
        email_subject = "Confirm your email @Bookalicious Login!!"
        message2 = render_to_string('accounts/email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],

        )

        email.fail_silently = True
        email.send()

        return redirect('register')

    return render(request, 'accounts/index_R.html')


# def loginapp(request):

#     if request.method == "POST":

#         username = request.POST.get('username')
#         pass1 = request.POST.get('pass1')

#         user = authenticate(username=username, password=pass1)
#         if user is not None:
#             login(request, user)
#             fname = user.first_name
#             return render(request, "main.html", {'fname': fname})
#         else:
#             messages.error(request, "Invalid Password")
#             return redirect('/loginapp')

#     return render(request, 'accounts/index_R.html')


# def signout(request):
#     logout(request)
#     messages.success(request, "Logged out Successfully")
#     return redirect('main')


def main(request):
    return render(request, 'Book/home.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('/')
    else:
        return render(request, 'accounts/activation_failed.html')
