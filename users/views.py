from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, ProfileUpdateForm
from django.contrib.auth import login
from django.core.mail import send_mail
import config.settings as settings
from .models import CustomUser


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('catalog:home')


class CustomLogoutView(LogoutView):
    next_page = 'catalog:home'


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать в наш сервис'
        message = 'Спасибо, что зарегистрировались в нашем сервисе!'
        recipient_list = [user_email]
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, recipient_list)


class ProfileUpdateView(UpdateView):
    model = CustomUser
    pk_url_kwarg = 'id'
    form_class = ProfileUpdateForm
    template_name = "users/update_profile.html"
    success_url = reverse_lazy('catalog:home')
