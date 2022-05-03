"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

import json
import os
import stripe

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email
from .settings import APP_FOLDER, APP_NAME

url_signer = URLSigner(session)

# Reads the stripe keys.
with open(os.path.join(APP_FOLDER, 'private', 'stripe_keys.json'), 'r') as f:
    STRIPE_KEY_INFO = json.load(f)
stripe.api_key = STRIPE_KEY_INFO['test_private_key']

def full_url(u):
    p = request.urlparts
    return p.scheme + "://" + p.netloc + u

@action('index')
@action.uses('index.html', db, auth, url_signer)
def index():
    return dict(
        # COMPLETE: return here any signed URLs you need.
        my_callback_url = URL('my_callback', signer=url_signer),
    )

@action('shopping_cart')
@action.uses('shopping_cart.html', db, auth, url_signer)
def shopping_cart():
    return dict(
        pay_url = URL('pay', signer=url_signer),
        stripe_key = STRIPE_KEY_INFO['test_public_key']
    )

@action('pay', method="POST")
@action.uses(db, url_signer)
def pay():
    line_items = []
    line_item = {
            'quantity': 1,
            'price_data': {
                'currency': 'usd',
                'unit_amount': 1599,
                'product_data': {
                    'name': "Super Cool Necklace",
                }
            }
    }
    line_items.append(line_item)

    stripe_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=full_url(URL('index')),
        cancel_url=full_url(URL('index')),
    )
    return dict(ok=True, session_id=stripe_session.id)