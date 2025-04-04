# from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .forms import ContactForm, ProductForm
from django.views.generic import ListView, FormView, CreateView
from .models import Product


class ProductsListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 8


class ContactView(FormView):
    template_name = 'catalog/contacts.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_success')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        return render(self.request, 'catalog/contact_success.html', {'name': name})


class ProductCreateView(CreateView):
    model = Product
    fields = ["name", "description", "image", "category", "price"]
    template_name = 'catalog/create_product.html'
    success_url = reverse_lazy('catalog:home')


# def home(request):
#     last_five_products = Product.objects.order_by('-created_at')[:5]
#     all_products = Product.objects.all()
#
#     paginator = Paginator(all_products, 8)  # Ограничиваем до 20 товаров на странице
#
#     page_number = request.GET.get('page')  # Получаем номер страницы из GET параметров
#     page_obj = paginator.get_page(page_number)  # Получаем нужную страницу
#
#     for product in last_five_products:
#         print(product)
#     return render(request, "home.html", {"products": page_obj})


# def contacts(request):
#     if request.method == "POST":
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#
#             return render(request, 'contact_success.html', {'name': name})
#     else:
#         form = ContactForm()
#
#     return render(request, 'contacts.html', {'form': form})


# def create_product(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('catalog:home')
#     else:
#         form = ProductForm()
#
#     return render(request, 'create_product.html', {'form': form})
