# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import date

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    email = models.CharField(max_length=32, default='')
    phone = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)

class Budget(models.Model):

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    user = models.ForeignKey(User)
    title = models.CharField(max_length=30, default='') # name of budget
    amount = models.IntegerField(default=0) # total amount to be set aside
    mode = models.NullBooleanField() # all at once or multiple disbursements
    interval = models.IntegerField(default=0) # days between disbursements
    frequency = models.IntegerField(default=0) # days(1), weeks(2), months(3), 30 days(4), year(5)
    freq_factor = models.IntegerField(default=0) # frequency factor or constant
    pay_value = models.IntegerField(default=0) # amount to be paid at individual disbursement
    pay_qty = models.IntegerField(default=0) # qty of individual disbursements
    pay_count = models.IntegerField(default=0) # count of last disbursement
    next_date = models.DateField(blank=False, null=False) # date of next disbursement to be made
    final_date = models.DateField(null=False, blank=True) # date of last disbursement
    budget_status = models.IntegerField(default=0) # 0=unpaid, 1=paid, 2=disbursement started, 3=disbursement complete, 4=other
    pay_ref = models.CharField(max_length=30, null=True) # Payment reference for funding a budget
    pay_status = models.CharField(max_length=10, null=True) # Status of payment attempt
    amount_funded = models.IntegerField(null=True) # amount funded for budget
    recipient = models.ForeignKey("Bank", blank=True, null=True) # actual account/destination budget is spent on
    recipient_code = models.CharField(max_length=20, blank=False) # required by Paystack
    created = models.DateTimeField(null=False)
    updated = models.DateTimeField(null=False)

class Bank(models.Model):
    def __unicode__(self):
        return self.holder_name, self.bank

    def __str__(self):
        return self.holder_name, self.bank

    holder_name = models.CharField(max_length=55, default="") # The account holder's name
    bank = models.CharField(max_length=55, default="") # The name of the bank
    bank_code = models.CharField(max_length=4, blank=True) # This used to be an IntegerField but ALAT code, 035A contains a character
    acc_no = models.CharField(max_length=10, blank=True) # The recipient (bank) account number
    created = models.DateTimeField(null=False)
    recipient_code = models.CharField(max_length=20, blank=False) # required by Paystack
    user = models.ForeignKey(User)

class Token(models.Model):
    def __unicode__(self):
        return self.user, self.last_4

    def __str__(self):
        return self.user, self.last_4
    last_4 = models.CharField(max_length=4, default='0000') # last 4 digits of card for reccognition
    auth_code = models.CharField(max_length=20, blank=True) #auth code to charge previously charged cards
    card_scheme = models.CharField(max_length=10, blank=True) # Card scheme of card e.g. Visa, MC, Verve
    user = models.ForeignKey(User)
