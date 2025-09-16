from django.shortcuts import render, redirect,get_object_or_404
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

def editStock(request, id):
    product = get_object_or_404(Product, id=id)  # use id
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('stockMang:stock')  # back to stock list
    else:
        form = ProductForm(instance=product)

    return render(request, 'stockMang/editStock.html', {'form': form})