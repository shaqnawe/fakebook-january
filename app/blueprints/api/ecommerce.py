from .import bp as app
import stripe
from flask import current_app, jsonify

stripe.api_key = current_app.config.get('STRIPE_TEST_SECRET_KEY')

@app.route('/products')
def get_products():
    print(stripe.Product.list()['data'])
    return jsonify([dict(
        id=p['id'],
        description=p['description'],
        image=p['images'][0],
        name=p['name'],
        price=stripe.Price.retrieve( p['metadata']['price'] )['unit_amount'],
    ) for p in stripe.Product.list()['data']])

@app.route('/product/<id>')
def get_product(id):
    # print(stripe.Product.list()['data'])
    return jsonify([dict(
        id=p['id'],
        description=p['description'],
        image=p['images'][0],
        name=p['name'],
        price=stripe.Price.retrieve( p['metadata']['price'] )['unit_amount'],
    ) for p in stripe.Product.list()['data']])