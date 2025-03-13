from django.shortcuts import render
from .forms import ContactForm


def home(request):
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
