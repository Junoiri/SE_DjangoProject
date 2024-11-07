from django.db import models
from django.db import models
from django.core.exceptions import ValidationError


def validate_positive(value):
    if value <= 0:
        raise ValidationError("The price must be a positive number.")


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive])
    available = models.BooleanField(default=True)


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField()


class Order(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In Process', 'In Process'),
        ('Sent', 'Sent'),
        ('Completed', 'Completed'),
    ]

    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(Product, related_name="orders")
    date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    def calculate_total_price(self):
        return sum(product.price for product in self.products.all())

    def can_fulfill_order(self):
        return all(product.available for product in self.products.all())
