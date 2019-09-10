from flask import Blueprint, render_template, request, redirect, url_for, flash
from main.utility import is_logged_in
import stripe

pub_key = 'pk_test_UnUu9uGYcKacbUqWioOZXUZn00YIWFkeEO'
secret_key = 'sk_test_lAWXy2zeGH9EWSA3toEYmPjq00JHUwiUwr'

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
