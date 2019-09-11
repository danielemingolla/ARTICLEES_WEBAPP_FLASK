from flask import Blueprint, render_template, request
from main.utility import is_logged_in
import stripe
import re

# Get Stripe's Api from credentials.txt
patternApi = re.compile(r'(\D\D_test_\w+)')
with open('credentials.txt', 'r') as f:
    contents = f.read()
    apiStripe = patternApi.findall(contents)
    pub_key = apiStripe[0]
    secret_key = apiStripe[1]
f.closed


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
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'], source=request.form['stripeToken'])
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=int(product.price)*100,
        currency='eur',
        description='WOMEN T-SHIRT UNIQUE SIZE'
    )
    return render_template('page/thanks.html', product=product)


@shopblueprint.route('/thanks')
def thanks():
    return render_template('page/thanks.html')
