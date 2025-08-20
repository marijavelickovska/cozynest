from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_product/', views.add_product, name='add_product'),
    #path('add_product_variant/<int:product_id>/', views.add_product_variant, name='add_product_variant'),
]
