# -*- coding: utf-8 -*-
from __future__ import unicode_literals # Has to be the first thing

# From registration email medium tutorial
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token


from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
# UserCreationForm - no longer required
from chris.forms import EditProfileForm, RegistrationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from django.urls import reverse
# import json

def login_redirect(request):
    # first two optoins don't work on their own. Should you always
    # use redirect with render?
    # return reverse("login")
    # return reverse("chris:login")
    return redirect(reverse("chris:login"))

def index(request):
    return reverse("login")

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Activate your blog account."
            message = render_to_string("acc_active_email.html", {
            "user": user,
            "domain": current_site.domain,
            "uid":urlsafe_base64_encode(force_bytes(user.pk)),
            "token":account_activation_token.make_token(user),
            })
            email_from = 'debola@budgetlikemagic.com'
            to_email = form.cleaned_data.get("email")
            send_mail(
                mail_subject,
                message,
                email_from,
                [to_email,],
                fail_silently=False,
            )
            context = {
                "message": "Please confirm your email address to complete registration"
            }
            return render(request, 'chris/register.html', context)
            # return render(request, 'chris/register.html')
    else:
        form = RegistrationForm()

        context = {'form': form}
        return render(request, 'chris/register.html', context)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        context = {
            "message": "email confirmed. Login now",
        }
        return render(request, 'chris/index.html', context)
    else:
        context = {
            "message": "Activation link is invalid",
        }
        return render(request, 'sprout/home.html')


def menu(request):
    return render(request, 'chris/menu.html')

def profile(request):
    context = {
        "user": request.user
    }
    return render(request, 'chris/profile.html', context)

def settings(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse("chris:profile"))
    else:
        form = EditProfileForm(instance=request.user)
        context = {
            "form": form
        }
        return render(request, 'chris/settings.html', context)

def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse("chris:profile"))
        else:
            return redirect(reverse("chris:change_password"))
    else:
        form = PasswordChangeForm(user=request.user)
        context = {
            "form": form
        }
        return render(request, 'chris/change_password.html', context)
