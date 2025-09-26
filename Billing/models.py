from django.db import models, transaction
from django.core.exceptions import ValidationError
from stockMang.models import Product


class Bill(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
    ]
    bill_number = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cash')

    def save(self, *args, **kwargs):
        if not self.bill_number:  # Only generate when creating
            with transaction.atomic():
                last_bill = Bill.objects.select_for_update().order_by('-id').first()
                if last_bill and last_bill.bill_number:
                    last_number = int(last_bill.bill_number.split('-')[-1])
                    new_number = last_number + 1
                else:
                    new_number = 1
                self.bill_number = f"CEEPEE-INVO-{new_number:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bill_number} - {self.customer_name}"

    @property
    def subtotal(self):
        """Sum of all item base prices (without tax)."""
        return sum(item.price * item.quantity for item in self.items.all())

    @property
    def tax_amount(self):
        """Total tax from all items."""
        return sum((item.price * item.quantity) * (item.tax_rate / 100) for item in self.items.all())

    @property
    def total_amount(self):
        """Subtotal + tax (final invoice amount)."""
        return self.subtotal + self.tax_amount


class BillItem(models.Model):
    bill = models.ForeignKey(Bill, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Store final unit price
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Store at time of sale

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.selling_price
        if not self.tax_rate:
            self.tax_rate = self.product.tax_rate

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
