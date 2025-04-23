# from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.shortcuts import render, reverse
from .forms import ContactForm, ProductForm
from django.views.generic import ListView, FormView, CreateView, UpdateView, DeleteView
from .models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory, BooleanField


# class StyleFormMixin:
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         for field in self.fields:
#             if isinstance(field, BooleanField):
#                 field.widget.attrs["class"] = "form-check-input"
#             else:
#                 field.widget.attrs["class"] = "form-control"


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


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    # fields = ["name", "description", "image", "category", "price"]
    template_name = 'catalog/create_product.html'
    success_url = reverse_lazy('catalog:home')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    pk_url_kwarg = 'id'
    template_name = 'catalog/delete_product.html'
    success_url = reverse_lazy('catalog:home')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    pk_url_kwarg = 'id'
    form_class = ProductForm
    template_name = "catalog/update_product.html"
    success_url = reverse_lazy('catalog:home')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     category_formset = inlineformset_factory(Product, Category, form=CategoryForm, extra=1)
    #
    #     if self.request.method == "POST":
    #         context["formset"] = category_formset(self.request.POST, instance=self.object)
    #     else:
    #         context["formset"] = category_formset(instance=self.object)
    #     return context
    #
    # def form_valid(self, form):
    #     context_data = self.get_context_data()
    #     formset = context_data["formset"]
    #
    #     if form.is_valid() and formset.is_valid():
    #         self.object = form.save()
    #         formset.instance = self.object
    #         formset.save()
    #         return super().form_valid(form)
    #     else:
    #         return self.render_to_response(self.get_context_data(form=form, formset=formset))


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
