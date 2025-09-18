# models.py

from django.db import models
from stockMang.models import Product
from django.core.exceptions import ValidationError

class Bill(models.Model):
    bill_number = models.CharField(max_length=20, unique=True)
    date = models.DateField(auto_now_add=True)
    customer_name = models.CharField(max_length=100)
    

    def __str__(self):
        return f"Bill {self.bill_number} - {self.customer_name}"

    @property
    def total_amount(self):
        return sum(item.total_amount for item in self.items.all())

class BillItem(models.Model):
    bill = models.ForeignKey(Bill, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Store final unit price
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Store at time of sale

    def save(self, *args, **kwargs):
        # Fetch price and tax from Product if not set
        if not self.price:
            self.price = self.product.selling_price
        if not self.tax_rate:
            self.tax_rate = self.product.tax_rate

        # Stock check and reduction
        if self.product.stock_quantity < self.quantity:
            raise ValidationError("Not enough stock!")
        self.product.stock_quantity -= self.quantity
        self.product.save()

        super().save(*args, **kwargs)

    @property
    def total_amount(self):
        base = self.price * self.quantity
        tax = base * (self.tax_rate / 100)
        return base + tax

    def __str__(self):
        return f"{self.quantity} x {self.product.name} @ {self.price}"
