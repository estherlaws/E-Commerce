from django.contrib import admin
from django.contrib.auth.models import User
from .models import ShippingAddress, Order, OrderItems

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItems)

# Create OrderItems Inline
class OrderItemsInline(admin.StackedInline):
    model = OrderItems
    extra = 0

# Extend Order Model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    fields = ["user", "full_name", "email", "shipping_address", "amount_paid", "date_ordered", "shipped"]
    inlines = [OrderItemsInline]

# Unregister Order Model
admin.site.unregister(Order)

# Re-Register Order And OrderAdmin
admin.site.register(Order, OrderAdmin)