# store/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Product 


def product_list(request):
  
    products = Product.objects.filter(is_active=True).order_by('name')

   
    context = {'products': products}


    return render(request, 'store/product_list.html', context)


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    cart = request.session.get('cart', {})
    product_id_str = str(product.id)
    
    
    current_cart_quantity = cart.get(product_id_str, 0)
    
   
    if current_cart_quantity >= product.stock_quantity:
        return redirect('product_list') 

    
    cart[product_id_str] = current_cart_quantity + 1
        
    
    request.session['cart'] = cart
   
    return redirect('product_list')

def cart_detail(request):
    
    cart = request.session.get('cart', {})
    product_ids = cart.keys()
    
    products = Product.objects.filter(id__in=product_ids)
   
    cart_items = []
    cart_total_price = 0
    
    for product in products:
        
        quantity = cart[str(product.id)]
       
        line_item_price = product.current_price * quantity
        cart_total_price += line_item_price
        
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'line_item_price': line_item_price,
        })

    context = {
        'cart_items': cart_items,
        'cart_total_price': cart_total_price,
    }
    return render(request, 'store/cart_detail.html', context)

@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        del cart[product_id_str] 
    
    request.session['cart'] = cart
    
    return redirect('cart_detail')


def checkout(request):
    
    if 'cart' in request.session:
        del request.session['cart']
        
    return render(request, 'store/checkout.html')