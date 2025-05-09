# from django.core.paginator import Paginator
from django.core.cache import cache
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ContactForm, ProductForm
from django.views.generic import ListView, FormView, CreateView, UpdateView, DeleteView, View
from .models import Product, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.contrib import messages
from .services import get_products_by_category
# from django.forms import inlineformset_factory, BooleanField


# class StyleFormMixin:
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         for field in self.fields:
#             if isinstance(field, BooleanField):
#                 field.widget.attrs["class"] = "form-check-input"
#             else:
#                 field.widget.attrs["class"] = "form-control"


class UnpublishProductView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        if not request.user.has_perm('catalog.can_cancel_publish_product') or product.owner != request.user:
            return HttpResponseForbidden("У вас нет прав для отмены публикации продукта.")

        product.is_published = False
        product.save()

        return redirect('catalog:home')


class ProductsListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 8

    # def get_queryset(self):
    #     category_pk = self.request.GET.get('category')
    #
    #     queryset = super().get_queryset()
    #
    #     if category_pk:
    #         category = get_object_or_404(Category, pk=category_pk)
    #         queryset = queryset.filter(category=category)
    #
    #     if not self.request.user.is_authenticated:
    #         queryset = queryset.filter(is_published=True)
    #
    #     return queryset

    def get_queryset(self):
        category_pk = self.request.GET.get('category')
        return get_products_by_category(category_pk, self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context


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

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    pk_url_kwarg = 'id'
    template_name = 'catalog/delete_product.html'
    success_url = reverse_lazy('catalog:home')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        obj = self.model.objects.filter(pk=kwargs['id']).first()

        is_manager = request.user.groups.filter(name='Менеджеры').exists()

        if obj.owner != request.user and not is_manager:
            messages.error(request, "Вы не можете удалить товар!")
            return redirect('catalog:home')
        return super().dispatch(request, *args, **kwargs)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    pk_url_kwarg = 'id'
    form_class = ProductForm
    template_name = "catalog/update_product.html"
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        obj = self.model.objects.filter(pk=kwargs['id']).first()

        is_manager = request.user.groups.filter(name='Менеджеры').exists()

        if obj.owner != request.user and not is_manager:
            messages.error(request, "Вы не можете изменять товар!")
            return redirect('catalog:home')
        return super().dispatch(request, *args, **kwargs)

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
