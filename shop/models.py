from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.quantity})"

    def can_purchase(self, amount=1):
        return self.quantity >= amount

    def purchase(self, amount=1):
        if amount <= 0:
            raise ValidationError("amount must be positive")
        if not self.can_purchase(amount):
            raise ValidationError("Товара недостаточно на складе")
        self.quantity -= amount
        self.save()

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'pk': self.pk})
