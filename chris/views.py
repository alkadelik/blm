# Best practice:
# Python first
# Django second
# Your apps
# Local directory

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from chris.forms import EditProfileForm, RegistrationForm
from django.contrib.auth import update_session_auth_hash, # login, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes, force_text
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.template.loader import render_to_string
# from .tokens import account_activation_token
# from django.core.mail import EmailMessage

def login_redirect(request):
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

# Registration with email host (zoho) that sends confirmation link to users
# def register(request):
#     if request.method == "POST":
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             mail_subject = "Activate your account."
#             message = render_to_string("acc_active_email.html", {
#                 "user": user,
#                 "domain": current_site.domain,
#                 "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#                 "token": account_activation_token.make_token(user),
#             })
#             to_email = form.cleaned_data.get("email")
#             email = EmailMessage(
#                 mail_subject, message, to=[to_email]
#             )
#             email.send()
#
#             context = {
#                 "screen_feedback": "Please confirm your email address to complete registration"
#             }
#             # return render(request, "chris/register.html", context)
#             return HttpResponse("Please confirm your email address to complete registration")
    # else:
    #     form = RegistrationForm()
    #
    #     context = {'form': form}
    #     return render(request, 'chris/register.html', context)

# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check.token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         # return redirect("home")
#         message = _("Thank you for confirming your email. You can log on")
#         request.user.message_set.create(message = message)
#         return redirect(reverse("chris:login"))
#     else:
#         message = _("Activation link is invalid")
#         request.user.message_set.create(message = message)
#         return redirect(reverse("chris:login"))

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
