from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    # barcode_code is auto-generated if not provided
    barcode_code = models.CharField(max_length=100, unique=True, blank=True)

    # Remove the ImageField - we generate barcodes in the browser now

    def save(self, *args, **kwargs):
        if not self.barcode_code:
            self.barcode_code = str(uuid.uuid4().int)[:12]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Sale(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='sales'
    )
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sold_at = models.DateTimeField(default=timezone.now)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.product.name} x{self.quantity} @ {self.sold_at.date()}"
