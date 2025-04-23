import config.settings as settings
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView
from django.views.decorators.http import require_POST
from .forms import MailingForm, LetterForm, RecipientForm
from .models import Mailing, Letter, Recipient
from django.urls import reverse_lazy
from django.core.mail import send_mail


class MailingListView(ListView):
    model = Mailing
    template_name = 'customers/mailing_list.html'
    context_object_name = 'mailing'


class MailingDetailView(DetailView):
    model = Mailing
    pk_url_kwarg = 'id'
    template_name = 'customers/mailing_detail.html'
    context_object_name = 'mailing'

    def get_object(self,  queryset=None):
        return super().get_object(queryset)

    def post(self, *args, **kwargs):
        mailing = self.get_object()

        recipients = mailing.recipients.all()
        emails = [recipient.email for recipient in recipients]

        self.send_notification_email(mailing, emails)

        return redirect("customers:mailing_list")

    def send_notification_email(self, mailing, emails):
        subject = mailing.letter.topic
        message = mailing.letter.content
        from_email = settings.EMAIL_HOST_USER
        recipient_list = emails

        send_mail(subject, message, from_email, recipient_list)


class MailingView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'customers/mailing.html'
    success_url = reverse_lazy('catalog:home')


class LetterView(CreateView):
    model = Letter
    fields = ['topic', 'content']
    template_name = 'customers/letter.html'
    success_url = reverse_lazy('catalog:home')


class RecipientView(CreateView):
    model = Recipient
    fields = ['email', 'full_name', 'comment']
    template_name = 'customers/recipient.html'
    success_url = reverse_lazy('catalog:home')
