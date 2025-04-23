from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            'username', 'email', 'countries', 'phone_number', 'avatar', 'mailing_confirmation', 'password1', 'password2'
        )

        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
            'countries': 'Страна проживания',
            'phone_number': 'Телефонный номер',
            'avatar': 'Фото профиля',
            'mailing_confirmation': 'Потвердить рассылку',
            'password1': 'Пароль',
            'password2': 'Потверждение пароля',
        }


class CustomAuthenticationForm(AuthenticationForm):
    pass
