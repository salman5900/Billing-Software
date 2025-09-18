from django.shortcuts import render

# Create your views here.
def BillingPage(request):
    return render(request, 'Billing/billing_home.html')