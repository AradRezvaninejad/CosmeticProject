
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("",views.index,name="index"),
    path('profile/', views.profile, name='profile'),
    path("signup/", views.signup_user, name="signup"),
    path("verify/", views.verify_email, name="verify_email"),
    path("login/", views.login_user, name="login"),  
    path("logout/", views.logout_user, name="logout_url"),
    path("product/<int:pk>/", views.product_page, name="product"),
    path("allproducts/",views.allproducts,name="allproducts"),
    path('category/<str:cat>/', views.category, name='category_url'),
    path('update_profile',views.update_profile,name="update_profile"),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
