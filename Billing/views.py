from django.shortcuts import render, redirect
from django.db import transaction
from django.forms import modelform_factory
from django.contrib import messages
from .models import Bill, BillItem
from .forms import BillForm, BillItemFormSet
from django import forms
from django.db.models import Sum

def BillingPage(request):
    if request.method == 'POST':
        bill_form = BillForm(request.POST)
        formset = BillItemFormSet(request.POST)
        if bill_form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    bill = bill_form.save()
                    items = formset.save(commit=False)
                    for item in items:
                        item.bill = bill
                        # Pulls product price and tax at time of billing
                        item.price = item.product.selling_price
                        item.tax_rate = item.product.tax_rate
                        # Checks again to prevent concurrent stock issue
                        if item.quantity > item.product.stock_quantity:
                            raise forms.ValidationError(
                                f"Not enough stock for {item.product.name}"
                            )
                        item.product.save()
                        item.save()
                    # formset.save_m2m()
                messages.success(request, 'Bill created successfully!')
                return redirect('Billing:dashboard')

            except Exception as e:
                print("M2M save error:", e)
                messages.error(request, f'Error: {e}')
        else:
            messages.error(request, 'Please correct errors below.')
    else:
        bill_form = BillForm()
        formset = BillItemFormSet()
    return render(request, 'Billing/billing_home.html', {
        'bill_form': bill_form,
        'formset': formset
    })


def dashboard(request):
    bills = Bill.objects.all().order_by('-date')
    total_revenue = sum(bill.total_amount for bill in bills)
    context = {
        'bills': bills,
        'total_revenue': total_revenue,
    }
    return render(request, 'Billing/dashboard.html', context)