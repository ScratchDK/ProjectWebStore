from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Создает или обновляет группу "Менеджеры" с нужными правами'

    def handle(self, *args, **kwargs):
        # Удаляем старую группу если существует
        Group.objects.filter(name="Менеджеры").delete()

        # Создаем новую группу
        group, created = Group.objects.get_or_create(name="Менеджеры")

        # Получаем нужные права
        content_type = ContentType.objects.get(app_label='catalog', model='product')
        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=[
                'add_product',
                'change_product',
                'delete_product',
                'view_product',
                'can_cancel_publish_product'
            ]
        )

        # Назначаем права группе
        group.permissions.set(permissions)

        self.stdout.write(
            self.style.SUCCESS(f'Группа "Менеджеры" успешно {"создана" if created else "обновлена"}')
        )
