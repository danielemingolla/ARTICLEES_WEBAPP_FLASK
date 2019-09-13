import stripe
import json
from articlee.models import Product
from articlee.config import read_json
from articlee.main.utility import is_logged_in
from flask import Blueprint, render_template, request


# Get Stripe's Api
pub_key, secret_key = read_json('pub_key_Stripe', 'sec_key_Stripe')

stripe.api_key = secret_key
shopblueprint = Blueprint('shopblueprint', __name__)

# Shop Main Page
@shopblueprint.route('/shop')
@is_logged_in
def shop():
    return render_template('page/shop.html', pub_key=pub_key)


@shopblueprint.route('/pay/<string:id>/', methods=['POST'])
def pay(id):
    # Get product
    product = Product.query.filter(Product.id == id).first()
    try:
        customer = stripe.Customer.create(
            email=request.form['stripeEmail'], source=request.form['stripeToken'])
        charge = stripe.Charge.create(
            customer=customer.id,
            amount=int(product.price)*100,
            currency='eur',
            description=product.name
        )
        return render_template('page/thanks.html', product=product)
    except:
        return render_template('page/405.html'), 405


@shopblueprint.route('/thanks')
def thanks():
    return render_template('page/thanks.html')
