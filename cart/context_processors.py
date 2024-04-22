from .cart import Cart

# Create context processor for functionality across all site pages
def cart(request):
    # Return default data from cart
    return {"cart": Cart(request)}