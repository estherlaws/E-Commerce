from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from store.models import Product
import datetime

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=50)
    shipping_email = models.EmailField(max_length=250)
    shipping_address1 = models.CharField(max_length=200)
    shipping_address2 = models.CharField(max_length=200, null=True, blank=True)
    shipping_city = models.CharField(max_length=50)
    shipping_state = models.CharField(max_length=20, null=True, blank=True)
    shipping_zipcode = models.CharField(max_length=5, null=True, blank=True)
    shipping_country = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f"Shipping Address - {str(self.id)}"
    
def create_shipping(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()

# Automates Profile Creation
post_save.connect(create_shipping, sender=User)
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=250)
    shipping_address = models.TextField(max_length=500)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    date_shipped = models.DateTimeField(blank=True, null=True)
    shipped = models.BooleanField(default=False)

    def __str__(self):
        return f"Order - {str(self.id)}"
    
@receiver(pre_save, sender=Order)

def update_shipped_date(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)

        if instance.shipped and not obj.shipped:
            instance.date_shipped = now


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = "Order Items"

    def __str__(self):
        return f"Order Items - {str(self.id)}"