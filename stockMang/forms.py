from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'hsn_code',
            'stock_quantity',
            'tax_rate',
            'selling_price',
            'dealer',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }