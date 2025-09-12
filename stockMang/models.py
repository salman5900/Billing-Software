from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    hsn_code = models.CharField(max_length=8, blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    # Store tax rate as a percentage, e.g., 18 for 18%
    tax_rate = models.DecimalField(max_digits=4, decimal_places=2, default=18.00) 
    # This is the taxable value / base price
    selling_price = models.IntegerField(default=0,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name



