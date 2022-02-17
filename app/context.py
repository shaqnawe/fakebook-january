from flask import current_app as app
from flask_login import current_user
import stripe

from app.blueprints.ecommerce.models import Cart

@app.context_processor
def cart_context():
    cart_dict = {}
    if current_user.is_anonymous:
        return {
            'cart_dict': cart_dict,
            'cart_size': 0,
            'cart_subtotal': 0,
            'cart_tax': 0,
            'cart_grandtotal': 0,
        }

    # find the user's cart
    cart = Cart.query.filter_by(user_id=current_user.id).all()
    if len(cart) > 0:
        for cart_item in cart:
            # get the product infor to be stored in the dictionary later
            stripeProduct = stripe.Product.retrieve(cart_item.product_id)
            print(stripeProduct)
            if cart_item.product_id not in cart_dict:
                cart_dict[stripeProduct.id] = {
                    'id': cart_item.id,
                    'product_id': stripeProduct.id,
                    'image': stripeProduct.images[0],
                    'quantity': 1,
                    'description': stripeProduct.description,
                    'price': stripe.Price.retrieve(stripeProduct['metadata']['price'])['unit_amount'],
                    # 'tax': stripeProduct.tax,
                }
            else:
                cart_dict[stripeProduct.id]['quantity'] += 1
    return {
            'cart_dict': cart_dict,
            'cart_size': sum([i.quantity for i in cart]),
            'cart_subtotal': 0,
            'cart_tax': 0,
            'cart_grandtotal': 0,
        }