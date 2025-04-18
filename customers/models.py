from django.db import models


# Получатель
class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    full_name = models.CharField(max_length=255, verbose_name='Ф.И.О.')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'

    def __str__(self):
        return self.full_name


# Письмо
class Letter(models.Model):
    topic = models.CharField(max_length=255, verbose_name='Тема письма')
    content = models.TextField(verbose_name='Содержание письма')

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'

    def __str__(self):
        return self.topic


# Рассылка
class Mailing(models.Model):
    STATUS_CHOICES = [
        ('Completed', 'Завершен'),
        ('Created', 'Создан'),
        ('Launched', 'Запущен'),
    ]

    # Дата и время начала рассылки
    first_mailing = models.DateTimeField(null=True, blank=True)

    # Дата и время окончания рассылки
    end_mailing = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Created')
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE, related_name='рассылки')
    recipients = models.ManyToManyField(Recipient, related_name='рассылки')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f"Рассылка от {self.first_mailing} - Статус: {self.status}"


class Attempt(models.Model):
    STATUS_CHOICES = [
        ('Successful', 'Успешно'),
        ('Unsuccessful', 'Не успешно'),
    ]

    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Unsuccessful', verbose_name='Статус')
    server_response = models.TextField(blank=True, verbose_name='Ответ почтового сервера')
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE, related_name='attempts', verbose_name='Рассылка')

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'

    def __str__(self):
        return f"Попытка рассылки {self.mailing} - Статус: {self.status} - Время: {self.attempt_time}"
