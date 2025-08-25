from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/<int:product_id>/', views.add_to_bag, name='add_to_bag'),
    path(
        'delete/<int:variant_id>/',
        views.delete_bag_item,
        name='delete_bag_item'
    ),
    path('edit/<int:variant_id>/', views.edit_bag_item, name='edit_bag_item'),
]
