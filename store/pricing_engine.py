# store/pricing_engine.py

# NOTE: We DO NOT import DiscountRule here to avoid the circular import.
# We import it INSIDE the function.

def calculate_dynamic_price(product):
    """
    Calculates the current price of a product based on active discount rules
    and the product's stock quantity.
    """
    # Import the model here to break the circular dependency
    from .models import DiscountRule 
    
    base_price = product.base_price
    final_price = base_price

    # 1. Fetch all active rules
    active_rules = DiscountRule.objects.filter(is_active=True).order_by('id')

    # 2. Iterate through rules and apply the first one that matches stock criteria
    for rule in active_rules:
        stock = product.stock_quantity

        if rule.min_stock <= stock <= rule.max_stock:

            if rule.rule_type == 'percent':
                discount_factor = 1 - rule.value
                final_price = base_price * discount_factor

            elif rule.rule_type == 'fixed':
                final_price = base_price - rule.value
                final_price = max(0, final_price) # Price cannot be negative

            # Apply the first match and stop
            return final_price

    # 3. If no rules match, return the original base price
    return final_price