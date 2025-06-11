from django.db import models
from datetime import date
from datetime import datetime
# from jalali_date import datetime2jalali
from django.utils import timezone
from main.models import Customer
# Create your models here.


#محصولات 
class Sub_category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.CharField(max_length=20)
    description = models.CharField(max_length=200)


    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.CharField(max_length=20)
    description = models.CharField(max_length=200)


    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, default=0, decimal_places=0)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=0, max_digits=12,null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Sub_category,on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="upload/products/")
    quantity = models.IntegerField(default=0)


    def __str__(self):
        return self.name
    
# banners
class banners(models.Model):
    title = models.CharField(max_length=50)
    big_content = models.CharField(max_length=255)
    small_content = models.CharField(max_length=255)
    button_text = models.CharField(max_length=100)
    related_value = models.CharField(max_length=255)
    related = models.CharField(max_length=255)
    picture = models.ImageField(upload_to="upload/banners/")
    def __str__(self):
        return self.title
#سفارشات

# class Order(models.Model):
#     product = models.ManyToManyField(Product)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     address = models.CharField(max_length=50)
#     date = models.DateField(default=datetime.now)
    
#     # def jalali_date(self):
#     #     return datetime2jalali(self.date).strftime('%Y/%m/%d')

#     def __str__(self):
#         return self.product

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderProduct')
    full_name = models.CharField(max_length=40 , blank=True)
    user_name = models.CharField(max_length=35, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=100,blank=True)
    total_price = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Order #{self.id} by {self.customer.user_name}"

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Transaction(models.Model):
    order = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)
    
    # def jalali_date(self):
    #     return datetime2jalali(self.date).strftime('%Y/%m/%d')
    

#blogzz

    
class Blog_position(models.Model):
    Position_choices = [
        ("1","normal"),
        ("2","khafan"),
        ("3","motevaset")
    ]
    position = models.CharField(max_length=2,choices=Position_choices,default=1)


class Blog(models.Model):
    title = models.CharField(max_length=200,null=True,unique=True)
    slug = models.SlugField(unique=True)  
    content = models.TextField(null=True)
    image = models.ImageField(upload_to='upload/blog_images/', blank=True, null=True)
    created = models.DateField(default=date.today)
    is_published = models.BooleanField(default=True)
    timeing = models.DateField(null=True)
    # def updated_at(self):
    #     return datetime2jalali(self.updated).strftime('%Y/%m/%d')
    
    # def created_at(self):
    #     return datetime2jalali(self.created).strftime('%Y/%m/%d')

    def __str__(self):
        return self.title
    
