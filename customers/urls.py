import customers.views as views
from django.urls import path
from customers.apps import CustomersConfig

app_name = CustomersConfig.name

urlpatterns = [
    path("", views.MailingListView.as_view(), name="mailing_list"),
    path('mailing_detail/<int:id>/', views.MailingDetailView.as_view(), name='mailing_detail'),
    path("mailing_create/", views.MailingView.as_view(), name="mailing_create"),
    path("letter/", views.LetterView.as_view(), name="letter"),
    path("recipient/", views.RecipientView.as_view(), name="recipient"),
]
