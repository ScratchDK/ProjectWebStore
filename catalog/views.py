from django.shortcuts import render
from .forms import ContactForm
from .models import Product


def home(request):
    last_five_products = Product.objects.order_by('-created_at')[:5]
    for product in last_five_products:
        print(product)
    return render(request, "home.html")


def contacts(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']

            return render(request, 'contact_success.html', {'name': name})
    else:
        form = ContactForm()

    return render(request, 'contacts.html', {'form': form})
