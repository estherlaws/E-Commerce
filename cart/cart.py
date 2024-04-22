from store.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session

        # Get current session key (if exists)
        cart = self.session.get("session_key")

        # If user is new, create session key
        if "session_key" not in request.session:
            cart = self.session["session_key"] = {}

        # Makes cart available on all site pages
        self.cart = cart

    def __len__(self):
        return len(self.cart)
    
    def cart_total(self):
        product_ids = self.cart.keys()

        # Lookup keys in DB model
        products = Product.objects.filter(id__in=product_ids)
        
        quantities = self.cart

        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)

        return total

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        # Cart Logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True


    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        ourcart = self.cart

        ourcart[product_id] = product_qty

        self.session.modified = True
        thing = self.cart
        return thing
    
    def delete(self, product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def get_prods(self):
        # Get IDs 
        product_ids = self.cart.keys()

        # Use IDs to lookup products in DB model
        products = Product.objects.filter(id__in=product_ids)

        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    