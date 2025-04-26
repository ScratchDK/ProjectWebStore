from django import forms
from .models import Product, Category
from django.core.exceptions import ValidationError


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100)
    email = forms.EmailField(label='Почта')
    message = forms.CharField(label='Сообщение', widget=forms.Textarea)


class ProductForm(forms.ModelForm):
    censorship = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price', 'unit', 'is_published']
        # widgets = {
        #     'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Введите описание продукта...'}),
        #     'price': forms.NumberInput(attrs={'step': '0.01'}),
        # }
        labels = {
            'name': 'Наименование',
            'description': 'Описание',
            'image': 'Изображение',
            'category': 'Категория',
            'price': 'Цена за покупку',
            'unit': 'Единица измерения',
            'is_published': 'Опубликовано',
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'placeholder': 'Введите название продукта'
        })

        self.fields['price'].widget.attrs.update({
            'step': '0.01'
        })

        self.fields['description'].widget.attrs.update({
            'rows': 8,
            'placeholder': 'Введите описание продукта...'
        })

        self.fields['category'].widget.attrs.update({
            'style': 'width: 100%'
        })

        self.fields['unit'].widget.attrs.update({
            'style': 'width: 100%'
        })

    def clean_name(self):
        product_name = self.cleaned_data.get("name")
        for word in ProductForm.censorship:
            if word in product_name.lower():
                raise ValidationError(f"Слово ({word}) нельзя использовать в наименовании продукта!")
        return product_name

    def clean_description(self):
        product_description = self.cleaned_data.get("description")
        for word in ProductForm.censorship:
            if word in product_description.lower():
                raise ValidationError(f"Слово ({word}) нельзя использовать в описании продукта!")
        return product_description

    def clean_price(self):
        product_price = self.cleaned_data.get("price")
        if product_price < 0:
            raise ValidationError(f"Цена не может быть отрицательной!")
        return product_price

    def clean_image(self):
        image = self.cleaned_data.get('image')

        # Проверяем, что изображение не None
        if image:
            if hasattr(image, 'content_type'):
                if image.content_type not in ['image/jpeg', 'image/png']:
                    raise ValidationError('Разрешены только файлы формата JPEG или PNG.')

                max_size = 5 * 1024 * 1024
                if image.size > max_size:
                    raise ValidationError('Размер файла не должен превышать 5 МБ.')

        else:
            raise ValidationError('Не выбрано ни одного изображения!')

        return image


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Введите описание продукта...'}),
        }
        labels = {
            'name': 'Наименование',
            'description': 'Описание'
        }
