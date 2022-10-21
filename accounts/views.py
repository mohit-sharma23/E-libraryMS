import uuid
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from .models import Profile
from .helpers import send_forget_password_mail
from django.contrib import messages


# Create your views here.
def account(request):

    return render(request, 'accounts/forget-password.html')


def ChangePassword(request, token):
    context = {}

    try:
        profile_obj = Profile.objects.filter(
            forget_password_token=token).first()
        context = {'user_id': profile_obj.user.id}
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request, 'No user id found.')
                return redirect(f'change-password/{token}/')

            if new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password/{token}/')

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            messages.success(
                request, 'Password has been changed successfully.')
            return redirect('login')

    except Exception as e:

        print(e)
    return render(request, 'accounts/change-password.html', context)


def ForgetPassword(request):

    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not User.objects.filter(username=username).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('/forget-password/')

            user_obj = User.objects.get(username=username)
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.get(user=user_obj)
            print(profile_obj)
            print(user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email, token)
            messages.success(request, 'An email is sent.')
            return redirect('/forget-password/')

    except Exception as e:
        print(e)
    return render(request, 'accounts/forget-password.html')
