from flask import flash, redirect, render_template, current_app, request, url_for
from flask_login import current_user
from app import db

from app.blueprints.ecommerce.models import Cart
from .import bp as app
import stripe
from app.context import cart_context

stripe.api_key = current_app.config.get('STRIPE_TEST_SECRET_KEY')

@app.route('/')
def products():
    # print(cart_context())
    # print(stripe.Product.list())
    products = [dict(
        id=p['id'],
        name=p['name'],
        description=p['description'],
        price=stripe.Price.retrieve(p['metadata']['price'])['unit_amount'] / 100,
        image=p['images'][0]
    ) for p in stripe.Product.list()['data']]
    # print(products)
    context = {
        'products': products
    }
    return render_template('ecommerce/products.html', **context)

@app.route('/products/add/<id>')
def add_product(id):
    # if the cart item exists inside of our cart_dict
    cart_item = Cart.query.filter_by(product_id=str(id)).filter_by(user_id=current_user.id).first()
    if cart_item:
        cart_item.quantity +=1
        db.session.commit()
    else:
        cart_item = Cart(product_id=str(id), user_id=current_user.id, quantity=1)
        db.session.add(cart_item)
        db.session.commit()
    flash(f'Product added to cart successfully', 'success')
    return redirect(url_for('ecommerce.products'))

@app.route('/products/cart/<id>')
def remove_product(id):
    # if the cart item exists inside of our cart_dict
    cart_item = Cart.query.filter_by(product_id=str(id)).filter_by(user_id=current_user.id).first()
    db.session.delete(cart_item)
    db.session.commit()
    flash(f'Product removed from the cart.', 'success')

    return redirect(url_for('ecommerce.cart'))

@app.route('/products/cart', methods=['POST'])
def update_cart():
    if request.method == 'POST':
        qtychanged = request.form.get('quantity')
        cart_item = Cart.query.filter_by(product_id=str(id)).filter_by(user_id=current_user.id).first()
        cart_item.quantity = qtychanged
        db.session.commit()
        flash(f'Shopping cart updated', 'success')
    return redirect(url_for('ecommerce.cart'))

@app.route('/products/cart')
def cart():
    cart_items = []
    for item in Cart.query.filter_by(user_id=current_user.id).all():
        stripe_product = stripe.Product.retrieve(item.product_id)
        product_dict = {
            'product': stripe_product,
            'price': stripe.Price.retrieve(stripe_product['metadata']['price'])['unit_amount'] / 100,
            'quantity': item.quantity
        }
        cart_items.append(product_dict)
    grand_total = 0
    if cart_items:
        for item in cart_items:
            grand_total +=  item['price']*item['quantity']
    
    context = {
        'cart': cart_items,
        'grand_total': (grand_total)
    }
    return render_template('ecommerce/cart.html', **context)

@app.route('/products/checkout', methods=['POST'])
def checkout():
    items = []
    for item in Cart.query.filter_by(user_id=current_user.id).all():
        stripe_product = stripe.Product.retrieve(item.product_id)
        product_dict = {
            'price': stripe.Price.retrieve(stripe_product['metadata']['price']),
            'quantity': item.quantity
        }
        items.append(product_dict)
    try:
        session = stripe.checkout.Session.create(
            line_items=items,
            mode='payment',
            success_url='http://localhost:5000/shop/products',
            cancel_url='http://localhost:5000/shop/products/checkout',
        )
    except Exception as error:
        return error

    # After successful payment, clear items from cart
    [db.session.delete(item) for item in Cart.query.filter_by(user_id=current_user.id).all()]
    db.session.commit()

    return redirect(session.url, code=303)