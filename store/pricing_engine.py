

# NOTE: We DO NOT import DiscountRule here to avoid the circular import.


def calculate_dynamic_price(product):
    """
    Calculates the current price of a product based on active discount rules
    and the product's stock quantity.
    """
    
    from .models import DiscountRule 
    
    base_price = product.base_price
    final_price = base_price

    active_rules = DiscountRule.objects.filter(is_active=True).order_by('id')

   
    for rule in active_rules:
        stock = product.stock_quantity

        if rule.min_stock <= stock <= rule.max_stock:

            if rule.rule_type == 'percent':
                discount_factor = 1 - rule.value
                final_price = base_price * discount_factor

            elif rule.rule_type == 'fixed':
                final_price = base_price - rule.value
                final_price = max(0, final_price) 

            return final_price

    return final_price