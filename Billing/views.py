from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages
from .models import Bill
from .forms import BillForm, BillItemFormSet
from django import forms
from .models import Bill
from django.db import transaction
# PDF generation imports
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.templatetags.static import static

def BillingPage(request):
    # Compute next bill number for display
    last_bill = Bill.objects.order_by('-id').first()
    if last_bill and last_bill.bill_number:
        try:
            last_number = int(last_bill.bill_number.split('-')[-1])
        except ValueError:
            last_number = 0
        next_bill_number = f"CEEPEE-INVO-{last_number + 1:04d}"
    else:
        next_bill_number = "CEEPEE-INVO-0001"

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
                        item.price = item.product.selling_price
                        item.tax_rate = item.product.tax_rate
                        if item.quantity > item.product.stock_quantity:
                            raise forms.ValidationError(
                                f"Not enough stock for {item.product.name}"
                            )
                        item.product.save()
                        item.save()
                    formset.save_m2m()

                # After saving, generate PDF
                logo_url = request.build_absolute_uri(static('images/logo.jpg'))
                html_string = render_to_string('Billing/bill_pdf.html', {'bill': bill, 'logo_url': logo_url})
                html = HTML(string=html_string)
                pdf_file = html.write_pdf()

                response = HttpResponse(pdf_file, content_type='application/pdf')
                response['Content-Disposition'] = f'filename=Invoice_{bill.bill_number}.pdf'
                return response

            except Exception as e:
                messages.error(request, f'Error: {e}')
        else:
            messages.error(request, 'Please correct errors below.')
    else:
        bill_form = BillForm()
        formset = BillItemFormSet()

    return render(request, 'Billing/billing_home.html', {
        'bill_form': bill_form,
        'formset': formset,
        'next_bill_number': next_bill_number
    })


def BillingPageEdit(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)

    if request.method == 'POST':
        bill_form = BillForm(request.POST, instance=bill)
        formset = BillItemFormSet(request.POST, instance=bill)

        if bill_form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    bill = bill_form.save()
                    items = formset.save(commit=False)

                    # Update items
                    for item in items:
                        item.bill = bill
                        item.price = item.product.selling_price
                        item.tax_rate = item.product.tax_rate
                        if item.quantity > item.product.stock_quantity:
                            raise forms.ValidationError(
                                f"Not enough stock for {item.product.name}"
                            )
                        item.product.save()
                        item.save()

                    # Delete items marked for removal
                    for obj in formset.deleted_objects:
                        obj.delete()

                messages.success(request, 'Bill updated successfully!')
                return redirect('Billing:dashboard')

            except Exception as e:
                print("Edit save error:", e)
                messages.error(request, f'Error: {e}')
        else:
            messages.error(request, 'Please correct errors below.')

    else:
        bill_form = BillForm(instance=bill)
        formset = BillItemFormSet(instance=bill)

    return render(request, 'Billing/billing_edit.html', {
        'bill_form': bill_form,
        'formset': formset,
        'edit_mode': True,
        'bill': bill,
    })

def BillingPageDelete(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    bill.delete()
    messages.success(request, 'Bill deleted successfully!')
    return redirect('Billing:dashboard')

def dashboard(request):
    bills = Bill.objects.all().order_by('-date')
    total_revenue = sum(bill.total_amount for bill in bills)
    context = {
        'bills': bills,
        'total_revenue': total_revenue,
    }
    return render(request, 'Billing/dashboard.html', context)
