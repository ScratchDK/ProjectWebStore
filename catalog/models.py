from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование', help_text='Введите наименование категории')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    UNIT_CHOICES = [
        ('Kilogram', 'кг'),
        ('Gram', 'гр'),
        ('Liter', 'л'),
        ('Piece', 'шт'),
        ('Package', 'уп')
    ]

    name = models.CharField(max_length=100, verbose_name='Наименование', help_text='Введите наименование продукта')
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='products/images/', blank=True, verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за покупку')
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, null=True, blank=True)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,  verbose_name='Старая цена')
    structure = models.TextField(blank=True, verbose_name='Состав')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['category']

    def get_unit_display(self):
        return dict(self.UNIT_CHOICES).get(self.unit, self.unit)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Сохраняем старую цену, если есть изменения
        if self.pk:  # Если объект уже существует в базе данных
            old_product = Product.objects.get(pk=self.pk)
            if old_product.price != self.price:
                self.old_price = old_product.price
        super(Product, self).save(*args, **kwargs)
