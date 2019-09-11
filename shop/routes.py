from flask import Blueprint, render_template, request
from main.utility import is_logged_in
import stripe
import json

# Get Stripe's Api from credentials.txt
with open('credentials.txt') as json_file:
    data = json.load(json_file)
    pub_key = data['pub_key_Stripe']
    secret_key = data['sec_key_Stripe']

stripe.api_key = secret_key
shopblueprint = Blueprint('shopblueprint', __name__)

# Shop Main Page
@shopblueprint.route('/shop')
@is_logged_in
def shop():
    return render_template('page/shop.html', pub_key=pub_key)


@shopblueprint.route('/pay/<string:id>/', methods=['POST'])
def pay(id):
    from models import Product
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
