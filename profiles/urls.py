from django.urls import path
from . import views


urlpatterns = [
    path('', views.profile, name='profile'),
    path('delivery_information', views.profile, name='delivery_information'),
    path('order_history', views.profile, name='order_history'),
]
