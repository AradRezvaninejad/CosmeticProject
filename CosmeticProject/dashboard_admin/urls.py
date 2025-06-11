from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from rest_framework.routers import DefaultRouter

urlpatterns = [
path("",views.dashboard_index, name="dashboard"),
path("order-detail/<str:id>",views.order_detail, name="order-detail"),
path("transactions",views.transactions, name="transactions"),
path("order-list",views.order_list, name="order-list"),
path("product-list",views.product_list, name="product-list"),
path("categories",views.categories, name="categories"),
path("sub_categories",views.sub_categories, name="sub_categories"),
path("add-product",views.add_products, name="add-product"),
path("profile",views.profile, name="profile"),
path("user-list",views.user_list, name="user-list"),
path("user-info/<str:username>",views.user_info, name="user-info"),
path("add_blog/",views.add_blog,name="add_blog"),
path("blog_list/",views.blog_list,name="blog_list"),
path("banners/",views.banners,name="banners"),
path("add_banner/",views.add_banner,name="add_banner"),
path("logout",views.logout, name="logout"),

]
