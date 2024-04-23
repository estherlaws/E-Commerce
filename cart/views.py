from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from store.models import Product
from .cart import Cart

def cart_summary(request):
    # Get cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    
    return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals})

def cart_add(request):
    # Get cart
    cart = Cart(request)

    # Test for post
    if request.POST.get("action") == "post":

        # Get product information
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))

        # Lookup product in database
        product = get_object_or_404(Product, id=product_id)

        # Save to Session
        cart.add(product=product, quantity=product_qty)

        # Get Cart Quantity
        cart_quantity = cart.__len__()

        # Return response
        response = JsonResponse({"qty": cart_quantity})
        messages.success(request, ("Product has been added to cart."))
        return response

def cart_update(request):
	cart = Cart(request)
	if request.POST.get("action") == "post":
        
		product_id = int(request.POST.get("product_id"))
		product_qty = int(request.POST.get("product_qty"))

		cart.update(product=product_id, quantity=product_qty)

		response = JsonResponse({"qty":product_qty})
		return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
          
          product_id = int(request.POST.get("product_id"))

          cart.delete(product=product_id)

          response = JsonResponse({"product":product_id})
          return response