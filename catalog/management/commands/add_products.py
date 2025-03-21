from django.core.management.base import BaseCommand
from catalog.models import Product
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Добавляет тестовые продукты и очищает существующие данные'

    def handle(self, *args, **kwargs):
        # Удаление всех существующих продуктов
        Product.objects.all().delete()

        call_command('loaddata', 'products_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))
