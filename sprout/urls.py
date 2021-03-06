from django.conf.urls import url
# from sprout.views import HomeView
from sprout import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name="home"), # Used with class based view
    url(r'^new_recipient/$', views.NewRecipient.as_view(), name="new_recipient"),
    url(r'^list_recipients/$', views.ListRecipients.as_view(), name="list_recipients"),
    url(r'^budgets/$', views.Budgets.as_view(), name="budgets"),
    url(r'^link_recipient/$', views.link_recipient, name="link_recipient"),
    url(r'^pay/$', views.pay, name="pay"),
    url(r'^payment_verification/$', views.payment_verification, name="payment_verification"),
    url(r'^send_email/$', views.send_email, name="send_email"),
    url(r'^transfer/$', views.transfer, name="transfer"),
    url(r'^resolve_account/$', views.resolve_account, name="resolve_account"),
    url(r'^add_recipient/$', views.add_recipient, name="add_recipient"),
    url(r'^budget_details/(?P<budget_id>\d+)/$', views.budget_details, name="budget_details"),
    url(r'^delete_budget/$', views.delete_budget, name="delete_budget"),
    url(r'^feedback/$', views.Feedback.as_view(), name='feedback'),
]
