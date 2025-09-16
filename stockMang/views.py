from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm
# Create your views here.
def stock(request):
    Products = Product.objects.all().order_by('-created_at')
    return render(request, 'stockMang/stockPage.html', {'products': Products})

def addStock(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stockMang:stock')
    else:
        form = ProductForm()
    return render(request, 'stockMang/addStock.html', {'form': form})