from django.shortcuts import render
from .models import Product
# Create your views here.
def stock(request):
    Products = Product.objects.all().order_by('-created_at')
    return render(request, 'stockMang/stockPage.html', {'products': Products})