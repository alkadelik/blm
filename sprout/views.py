# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.mail import send_mail
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from sprout.forms import BudgetSetupForm, NewRecipientForm
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import date, datetime, timedelta
from django.urls import reverse
from chris.models import Budget, Bank, Token

from django.http import JsonResponse
import requests, json # requests was installed by pip

class HomeView(TemplateView):
    template_name = "sprout/home.html"

    # Form to be able to tell what information is requred depending on the mode
    # i.e. one-off or multiple disbursements. For now, we assume multiple
    def post(self, request):
        if request.method == "POST":
            new_budget = Budget()
            new_budget.user = request.user
            new_budget.created = timezone.now()
            new_budget.updated = timezone.now()

            # From form:
            try:
                amount = int(request.POST["amount"]) * 100 # amount always in kobo
                next_date = datetime.strptime(request.POST["next_date"], "%Y-%m-%d")
                new_budget.title = request.POST["title"]
            except:
                # Nothing has been posted
                return redirect("sprout:home")

            new_budget.next_date = next_date
            new_budget.mode = "1"
            # new_budget.mode = request.POST["mode"]
            new_budget.amount = amount # have to override the entry from the model form

            if new_budget.mode == "1": # It means this is a one-off payment
                # No frequency, frequency factor or pay_qty, thus, do not display them
                # Is it tautology setting them to None here even though they were never set
                new_budget.freq_factor = 0
                new_budget.frequency = 0
                new_budget.pay_qty = 1
                new_budget.pay_value = amount
                new_budget.final_date = next_date
                new_budget.save()
            # elif new_budget.mode == "0": # Multiple disburesments
            #     pay_qty = int(request.POST["pay_qty"])
            #     frequency = request.POST["frequency"]
            #     freq_factor = int(request.POST["freq_factor"])
            #
            #     new_budget.freq_factor = freq_factor
            #     new_budget.frequency = frequency
            #     new_budget.pay_qty = pay_qty
            #     new_budget.pay_value = amount/pay_qty
            #     # The user may be confused as to how the math is done becuase quotient is being used
            #     # pay_qty = amount//interval
            #
            #     # convert frequency to number of days (if days, weeks, or 30 days)
            #     if frequency == "1":
            #         global interval
            #         interval = 1 * freq_factor
            #         new_budget.interval = interval
            #     elif frequency == "2":
            #         global interval
            #         interval = 7 * freq_factor
            #         new_budget.interval = interval
            #
            #     new_budget.final_date = next_date + timedelta(days=(interval*(pay_qty-1)))
            #     new_budget.save()

            request.session["budget_id"] = new_budget.id

            return redirect("sprout:list_recipients")

        else:
            return render(request, self.template_name)


# Populates the recepient (bank) options for users select
class NewRecipient(TemplateView):
    template_name = "sprout/new_recipient.html"


    def get(self, request):
        headers = {
            "Authorization": "Bearer sk_live_01ee65297a9ae5bdf8adbe9ae7cdf6163384a00e",
        }
        bank_list_url = "https://api.paystack.co/bank"
        response = requests.request("GET", bank_list_url, headers=headers).json()

        response = response["data"]

        context = {
            "banks": response,
            "user_id": self.request.user.id , # figure out how best to send this for secuirty
        }
        return render(request, self.template_name, context)

# Verifies that the recipient details (bank and account no) are valid
def resolve_account(request):
    headers = {
        "Authorization": "Bearer sk_live_01ee65297a9ae5bdf8adbe9ae7cdf6163384a00e",
    }

    if request.method == "POST":
        acc_no = request.POST["acc_no"]
        bank_code = request.POST["bank_code"]

        api = "https://api.paystack.co/bank/resolve?account_number="

        api_string = "&bank_code="

        url = api + acc_no + api_string + bank_code
        response = requests.request("GET", url, headers=headers).json()

    try:
        holder_name = response["data"]["account_name"]
        # recipient_code = respons["data"]["recipient_code"]
        response = holder_name

    except:
        unresolved_message = response["message"]
        response = unresolved_message,

    # need to figure out how to send this back to the template
    return JsonResponse(response, safe=False)
    # return render(request, "sprout/new_recipient.html", context)

# Adds the new reciient (bank) details to the user's database
# Is this better populated with values from new_recipient.html
# or with values from resolve_account(request)?
def add_recipient(request):
    if request.method == "POST":
        acc_no = request.POST["acc_no"]
        bank_code = request.POST["bank_code"]
        bank_name = request.POST["bank_name"]
        holder_name = request.POST["holder_name"] # Figure out the
            # best way to do this

        # at this point, a transfer recipient should be created
        url = "https://api.paystack.co/transferrecipient"
        headers = {
            # "Authorization": "Bearer sk_test_7cb2764341285a8c91ec4ce0c979070188be9cce",
            "Authorization": "Bearer sk_live_01ee65297a9ae5bdf8adbe9ae7cdf6163384a00e"
        }

        # This is updating my live user
        data = {
            'type': "nuban",
            'name': holder_name,
            'description': "Budget title",
            'account_number': acc_no,
            'bank_code': bank_code,
            "currency": "NGN",
            "metadata": {
                "job": "Flesh Eater",
            }
        }
        response = requests.post(url, json=data, headers=headers).json()
        recipient_code = response["data"]["recipient_code"]


        new_recipient = Bank(holder_name=holder_name, bank=bank_name,
            bank_code=bank_code, acc_no=acc_no,
            created=timezone.now(), user_id=request.user.id, recipient_code=recipient_code)
            # recipient_code appears in two Bank and Budget tables: refactor
        new_recipient.save()

        try:
            current_budget_id = request.session["budget_id"]
            budget = Budget.objects.get(id=current_budget_id)
            if budget.recipient_id is None:
                budget.recipient_id = new_recipient.id
                budget.recipient_code = recipient_code
                budget.save()
                # clear current_budget_id
                # del request.session["budget_id"]
                return redirect("sprout:pay")
        except:
            # This exception means there is no budget_id set
            print "You have successfully added a recipient..."
        return redirect("sprout:home")
        # This redirect means there is a budget_id set
        # but the budget already has a recipient
        # if the budget hasn't been funded, user can fund
        # or return recipients list or budget list depending
        # on where they came from
    else:
        # "What to do if form is not not post?"
        pass

    # return render(request, "sprout/list_recipients.html")
    return redirect("/sprout/")
    # return render(request, "sprout:new_recipient", context)

class ListRecipients(TemplateView):
    template_name = "sprout/list_recipients.html"

    # Note that this can be coming from a newly created budget
    # or from an existing, but unlinked, one.
    # Check to see if an ID already exists then set the session for the new ID.
    # What happens if the user doesn't go on to do anything with the ID?

    def post(self, request):
        if request.method == "POST":
            budget_id = request.POST["budget_id"]
            request.session["budget_id"] = budget_id

            user_id = request.user.id
            banks = Bank.objects.filter(user_id=user_id)

            context = {
                "banks": banks,
                "budget_id": budget_id,
            }
            # return redirect("sprout:list_recipients")
            return render(request, self.template_name, context)

    def get(self, request):
        user_id = request.user.id
        banks = Bank.objects.filter(user_id=user_id)

        context = {
            "banks": banks,
        }
        return render(request, self.template_name, context)

def link_recipient(request):
    try:
        budget_id = request.session["budget_id"]
        if request.method == "POST":
            recipient_id = request.POST["recipient_id"]
            # Improve below to get recipient_code from form rather than call
            # Bank table
            recipient = Bank.objects.get(id=recipient_id)
            recipient_code = recipient.recipient_code

            # Is there a chance the budget already has a recipient_id and code?
            budget = Budget.objects.get(id=budget_id)
            budget.recipient_id = recipient_id
            budget.recipient_code = recipient_code
            budget.save()
            return redirect("sprout:pay")
    except:
        print "There is no budget to link recipient to"
    return redirect("sprout:home")

def pay(request):
    # if request.session["budget_id"]:
    try: # if id sent from frontend.
        if request.method == "POST":
            request.session["budget_id"] = request.POST["budget_id"]
    except:
        pass

    try:
        current_budget_id = request.session["budget_id"]
        budget = Budget.objects.get(id=current_budget_id)
        user = request.user

        linked_account = Bank.objects.get(id=budget.recipient_id)

        def mode():
            if budget.mode == 1: # Single disbursement
                return "One off"
            elif budget.mode == 0: # Multiple disbursements
                return "Multiple disbursements"

        context = {
            # "pk": "pk_test_9b841d2e67007aeca304a57442891a06ad312ece",
            "pk": "pk_live_163e7cf486ffc7c6458472600beea80901168692",
            "email": request.user.email,
            "mode": mode(),
            "currency": "NGN",
            "budget": budget,
            "linked_account": linked_account,
        }
        return render(request, "sprout/pay.html", context)
    except:
        return redirect("sprout:home")
        # should this redirect anywhere else?

# class PaymentVerification(TemplateView):
#     template_name = "sprout/"
def payment_verification(request):
    api = "https://api.paystack.co/transaction/verify/"
    headers = {
        # 'Authorization': "Bearer sk_test_7cb2764341285a8c91ec4ce0c979070188be9cce",
        'Authorization': "Bearer sk_live_01ee65297a9ae5bdf8adbe9ae7cdf6163384a00e",
    }

    if request.method == "POST":
        pay_ref = request.POST["pay_ref"]

        url = api + pay_ref
        response = requests.request("GET", url, headers=headers).json()
        auth_code = response["data"]["authorization"]["authorization_code"]
        brand = response["data"]["authorization"]["brand"]
        last_4 = response["data"]["authorization"]["last4"]

        pay_status = response["status"]
        if pay_status == True:
            current_budget_id = request.session["budget_id"]
            budget = Budget.objects.get(id=current_budget_id)
            budget.pay_status = response["data"]["status"]

            if budget.pay_status == "success":
                budget.pay_ref = response["data"]["reference"]
                budget.amount_funded = response["data"]["amount"]
                # check that amount funded equals budget amount
                budget.budget_status = 1
                budget.save()

                # Check if token already exists for card
                try:
                    token = Token.objects.get(auth_code=auth_code)
                except:
                    # First ask user if they'd like to save card
                    new_token = Token(last_4=last_4, auth_code=auth_code, card_scheme = brand, user_id=request.user.id)
                    new_token.save()

                # Send success email to recipient
                # Ideally send it to a queue here
                mail_subject = "You've funded your budget"
                email_template = "budget_funded_email.html"
                email_from = "yass@budgetlikemagic.com"
                to_email = request.user.email

                message = render_to_string(email_template, {
                    "amount": budget.amount_funded,
                    "budget": budget.title,
                })

                send_mail(
                    mail_subject,
                    message,
                    email_from,
                    [to_email,],
                    fail_silently=False,
                )

                del request.session["budget_id"]
            else:
                # Wait for webhook
                budget.pay_ref = response["data"]["reference"]

        return redirect("/sprout/")

def charge_auth(request):
    url = "https://api.paystack.co/transaction/charge_authorization"
    headers = {
        # 'Authorization': "Bearer sk_test_7cb2764341285a8c91ec4ce0c979070188be9cce",
        'Authorization': "Bearer sk_live_01ee65297a9ae5bdf8adbe9ae7cdf6163384a00e",
    }
    data = {
        # {"authorization_code": "AUTH_67wpn7vbtq",
        # "email": request.user.email,
        # "amount": 500000,
        # "custom_fields": [{
        #     "Budget": budget name,
        #     }]
        }
    response = requests.post(url, json=data, headers=headers).json()
    # recipient_code = response["data"]["recipient_code"]
    return None

def transfer(request):
    url = "https://api.paystack.co/transfer/bulk"
    headers = {
        # "Authorization": "Bearer sk_test_7cb2764341285a8c91ec4ce0c979070188be9cce",
        "Authorization": "Bearer sk_live_01ee65297a9ae5bdf8adbe9ae7cdf6163384a00e"
    }

    # Consider making it such that all budgets that are stored in the db where a next_date
    # must have been funded, or are purged at some point. This saves us from filtering
    # non-serious budgets

    today = datetime.today()
    due_payments = Budget.objects.filter(budget_status__gte=1, budget_status__lt=3,
        next_date__year=today.year,
        next_date__month=today.month,
        next_date__day=today.day
        )
        # Is there an advantage to also filter by pay_count < pay_qty
        # or does the status filter suffice for this?

    transfers = []
    to_update = []
    for budget in due_payments:
        # transfers = [{}, {}]
        transfer = {"amount": budget.pay_value, "recipient": budget.recipient_code}
        params = {
            "budget_id": budget.id,
            "budget_title": budget.title, # reserve this for reason
            "budget_status": budget.budget_status,
            "pay_count": budget.pay_count,
            "pay_qty": budget.pay_qty,
            "interval": budget.interval
        }
        transfers.append(transfer)
        to_update.append(params)

    # Sending to the transfers API
    data = {
        "currency": "NGN",
        "source": "balance",
        "transfers": transfers,
    }
    # feedback for Paystack. If one recipient_code is false (or absent),
    # continue with the others na, rather than null everything
    response = requests.post(url, json=data, headers=headers).json()

    # After payment: Update the budget status and next date in db
    if response["status"] == True:
    # Better yet, check that the number of transfers queued is equal to the number of
    # transfers sent i.e. the number in `response["message"]`
        for budget in due_payments:
            # is the order in whicn they are retrieved from the database the same
            # as the order they are here?
            budget.pay_count += 1
            if budget.pay_count < budget.pay_qty:
                budget.budget_status = 2
                budget.next_date = today + timedelta(days=(budget.interval))
                budget.save()
            elif budget.pay_count == budget.pay_qty:
                budget.budget_status = 3
                budget.save()

            # Send success email to recipient
            mail_subject = budget.title + " disbursement"
            template = "budget_disbursed_email"
            email_from = "help@budgetlikemagic.com",
            to_email = request.user.email

            message = render_to_string(email_template, {
            # "user": user, # context can be passed to the message
            })

            send_mail(
                mail_subject,
                message,
                email_from,
                [to_email,],
                fail_silently=False,
            )
    else:
        print "Transfers failed with message:", response["message"]

    return redirect(reverse("sprout:home"))
    # return render(request, "sprout/list_recipients.html")

class Budgets(TemplateView):
    template_name = "sprout/budgets.html"

    def get(self, request):
        user_id = request.user.id
        my_budgets = Budget.objects.filter(user_id=user_id).order_by('-created')
        unfunded_budgets = my_budgets.filter(budget_status=0)
        active_budgets = my_budgets.filter(budget_status__gte=1, budget_status__lt=3,)
        finished_budgets = my_budgets.filter(budget_status=3)

        context = {
            "my_budgets": my_budgets,
            "active_budgets": active_budgets,
        }
        return render(request, self.template_name, context)

def budget_details(request, budget_id):
    if budget_id is not None:
        budget = Budget.objects.get(id=budget_id)
        if budget.user_id == request.user.id:
            context = {"budget": budget}
            return render(request, "sprout/budget_details.html", context)
        else:
            return redirect("sprout:budgets")

class Feedback(TemplateView):
    template_name = "sprout/feedback.html"

    def get(self, request):
        return render(request, self.template_name)

def delete_budget(request):
    if request.method == "POST":
        budget_id = request.POST["budget_id"]
        Budget.objects.filter(id=budget_id).delete()
        return redirect("sprout:budgets")

def send_email(request):
    mail_subject = "Test mail is working"
    message = render_to_string("test_email.html")
    email_from = "me@budgetlikemagic.com"
    to_email = "debola_adeola@yahoo.com"

    send_mail(
        mail_subject,
        message, # figure this from post
        email_from, # figure this from post
        [to_email,],
        fail_silently=False,
    )
    return redirect("sprout:budgets")

    # if request.method == "POST":
    #     mail_subject = request.POST["mail_subject"]
    #     template = request.POST["template"] # This is a link to a message
    #     email_from = request.POST["email_from"]
    #     email_context = request.POST["email_context"]
    #     to_email = request.user.email
    #
    #     if template == "budget_funded_email":
    #         email_template = "budget_funded_email.html"
    #         ## email is from payment
    #         email_from = "help@budgetlikemagic.com"
    #     elif template == "other_template_yet_decided":
    #         email_template = "other_email_template.html"
    #         email_from = "other@budgetlikemagic.com"
    #     else:
    #         pass
    #
    #     message = render_to_string(email_template, {
    #     # "user": user, # context can be passed to the message
    #     })
    #
    #     send_mail(
    #         mail_subject,
    #         message, # figure this from post
    #         email_from, # figure this from post
    #         [to_email,],
    #         fail_silently=False,
    #     )
    #     return redirect("sprout:budgets")
