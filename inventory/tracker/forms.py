from django.forms import ModelForm

from inventory.tracker.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ('qty', )
