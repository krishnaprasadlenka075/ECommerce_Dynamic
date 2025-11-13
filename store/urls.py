# store/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    # 💡 NEW LINE 1: Path to remove an item from the cart
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'), 
    # 💡 NEW LINE 2: Path for the final checkout process
    path('checkout/', views.checkout, name='checkout'), 
]