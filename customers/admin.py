from django.contrib import admin
from .models import Mailing, Letter


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('first_mailing', 'end_mailing', 'status', 'letter')
    list_filter = ('status',)
    search_fields = ('letter', 'recipients',)


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ('topic', 'content')
    search_fields = ('topic', 'content',)
