from django.contrib import admin
from .models import Customer,Product,Category

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)