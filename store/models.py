
from django.db import models
from django.core.validators import MinValueValidator
from .pricing_engine import calculate_dynamic_price


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    
    base_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    
    
    current_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    stock_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    
    def save(self, *args, **kwargs):
        self.current_price = calculate_dynamic_price(self)
        super().save(*args, **kwargs)


class DiscountRule(models.Model):
    name = models.CharField(max_length=100)
    
    rule_type = models.CharField(max_length=20, choices=[('percent', 'Percentage Off'), ('fixed', 'Fixed Amount Off')])
    
    
    value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Percentage (e.g., 0.10 for 10%) or Fixed amount")
    
    min_stock = models.IntegerField(default=0, help_text="Apply only if stock is above this level")
    max_stock = models.IntegerField(default=999999, help_text="Apply only if stock is below this level")
    
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name