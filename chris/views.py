# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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

# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse("sprout:home"))
#     else:
#         form = UserCreationForm()
#
#         context = {'form': form}
#         return render(request, 'chris/register.html', context)

# This registers using a custom reg form - also commented out in forms
# See tutorial 16 Max Goodridge Django tutorials
def email(request):
    subject = "Thank you for registering to our site"
    message = "It means a world to us"
    email_from = 'debola@budgetlikemagic.com'
    recipient_list = ['debola_adeola@yahoo.com',]

    send_mail(
    # email = EmailMessage(
        "Thank you for registering to our site",
        "It means a world to us",
        'debola@budgetlikemagic.com',
        ['debola_adeola@yahoo.com',],
        fail_silently=False,
    )
    # email.send()

    return render(request, 'chris/login.html')

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/sprout")
    else:
        form = RegistrationForm()

        context = {'form': form}
        return render(request, 'chris/register.html', context)

# Moved to new app
# def home(request):
#     return render(request, 'chris/home.html')

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
