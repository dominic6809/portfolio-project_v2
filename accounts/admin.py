from django.contrib import admin

from . models import Customer, Order, Product, Manufacturer, Tag

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Tag)
admin.site.register(Manufacturer)