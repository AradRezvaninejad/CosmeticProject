from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Sub_category)

admin.site.register(banners)

admin.site.register(Order)
admin.site.register(Transaction)
admin.site.register(OrderProduct)
admin.site.register(Blog)
admin.site.register(Blog_position)