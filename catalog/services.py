from django.core.cache import cache
from django.shortcuts import get_object_or_404
from .models import Product, Category


def get_products_by_category(category_pk=None, user=None):
    """Сервисная функция для получения продуктов по категории"""
    cache_key = f"products_category_{category_pk}_auth_{user.is_authenticated if user else False}"
    queryset = cache.get(cache_key)

    if queryset is None:
        queryset = Product.objects.prefetch_related('category')

        if category_pk:
            category = get_object_or_404(Category, pk=category_pk)
            queryset = queryset.filter(category=category)

        if user and not user.is_authenticated:
            queryset = queryset.filter(is_published=True)

        cache.set(cache_key, queryset, timeout=900)

    return queryset
