# forms.py

from django import forms
from django.forms import inlineformset_factory
from .models import Bill, BillItem

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['bill_number', 'customer_name']
        exclude = ['bill_number']  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'border border-gray-300 rounded p-2 w-full'})

class BillItemForm(forms.ModelForm):
    class Meta:
        model = BillItem
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'border border-gray-300 rounded p-1 w-full'})

    def clean_quantity(self):
        qty = self.cleaned_data['quantity']
        product = self.cleaned_data.get('product')
        if product and qty > product.stock_quantity:
            raise forms.ValidationError("Not enough stock for this product.")
        return qty

BillItemFormSet = inlineformset_factory(
    Bill, BillItem, form=BillItemForm, extra=1, min_num=1, validate_min=True, can_delete=True
)
