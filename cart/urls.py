from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path("", views.cart_summery, name="cart"),
    path("add/", views.cart_add, name="add_to_cart"),
    path("remove/", views.cart_delete, name="remove_from_cart"),
    path("update/", views.cart_update, name="update_cart"),
    # path('request/', views.send_request, name='request'),
    # path('verify/', views.verify , name='verify'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
