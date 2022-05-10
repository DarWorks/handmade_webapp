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

###############################################################################

#//////////////////////////////////////////////////////////
# HOMEPAGE
#//////////////////////////////////////////////////////////


@action('homepage')
@action.uses('homepage.html',  url_signer, db, auth)
def index():
    print("serving homepage")
    # TODO: display products and info from the database later
    return dict(
        # COMPLETE: return here any signed URLs you need.
        my_callback_url = URL('my_callback', signer=url_signer),
    )


@action('index')
@action.uses('index.html', db, auth, url_signer)
def index():
    # TODO: this is just a short term solution, needs to be changed
    redirect(URL('homepage'))
    return dict(
        # COMPLETE: return here any signed URLs you need.
        my_callback_url = URL('my_callback', signer=url_signer),
    )

#//////////////////////////////////////////////////////////
# LOGIN/REGISTRATION
#//////////////////////////////////////////////////////////


@action('loginH')
@action.uses('loginH.html', url_signer,auth.user, db, session)
def index():
    print("serving login")
    return dict(
        # COMPLETE: return here any signed URLs you need.
        my_callback_url = URL('my_callback', signer=url_signer),
    )


@action('regisH')
@action.uses('registrationH.html', url_signer, auth.user, db, session)
def index():
    print("serving registration")
    return dict(
        # COMPLETE: return here any signed URLs you need.
        my_callback_url = URL('my_callback', signer=url_signer),
    )


#//////////////////////////////////////////////////////////
# SHOPPING CART
#//////////////////////////////////////////////////////////

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


#//////////////////////////////////////////////////////////
# PROFILE PAGE
#//////////////////////////////////////////////////////////


@action('profile/<username>')
@action.uses('profile.html', auth, url_signer)
def profile(username=None):
    assert username is not None
    user = auth.get_user()
    # TODO: grab product data from DB using username
    # Then serialize the data in the format that is used in the html template like shown below
    # NOTE: we only need the first image for each product
    # ALSO ADD username field in auth
    return dict(
        my_callback_url = URL('my_callback', signer=url_signer),
        isAccountOwner= (user is not None) and (user.get('username', '') == username),
        profile = dict(
            username= username,
            total_credits=112,
            profile_pic= "images/profile/image1.png"
        ),
        selling = (
            dict(
                id="123",
                seller="SellerUsername",
                image="images/product/image1.png"
            ),
            dict(
                id="123",
                seller="SellerUsername",
                image="images/product/image1.png"
            ),
            dict(
                id="123",
                seller="SellerUsername",
                image="images/product/image1.png"
            )
        ),
        purchased = (
            dict(
                id="123",
                seller="SellerUsername",
                image="images/product/image1.png"
            ),
            dict(
                id="123",
                seller="SellerUsername",
                image="images/product/image1.png"
            )
        )
    )


@action('add_product')
@action.uses('add_product.html', db, auth, url_signer)
def add_product():
    return dict(
        add_product_info_url = URL('add_product_info'),
    )

@action('add_product_info', method=['POST'])
@action.uses(db)
def add_product_info():
    id = db.products.insert(
    name=request.json.get('product_name'),
    # ADD REFERENCE TO SELLER ID
    type=request.json.get('product_type'),
    description=request.json.get('product_description'),
    price=request.json.get('product_price'),
    image1=request.json.get('product_image1'),
    )
    return dict(id=id)


#//////////////////////////////////////////////////////////
# PRODUCT PAGE
#//////////////////////////////////////////////////////////


@action('product/<seller_name>/<product_id:int>')
@action.uses('product.html', auth, url_signer)
def product(seller_name=None, product_id=None):
    assert product_id is not None
    assert seller_name is not None
    data = db(db.products.id == product_id).select()
    prod = data.first()
    if prod is None:
        return "404 Not found"
    data = db(db.userProfile.id == prod.seller).select()
    sellerProfile = data.first()
    if sellerProfile is None or sellerProfile.username != seller_name:
        return "404 Not found"
    images = []
    if prod.image1 is not None:
        images.append(prod.image1)
    if prod.image2 is not None:
        images.append(prod.image2)
    if prod.image3 is not None:
        images.append(prod.image3)
    if prod.image4 is not None:
        images.append(prod.image4)
    return dict(
        my_callback_url = URL('my_callback', signer=url_signer),
        get_comments_url = URL('comments', product_id),
        get_reviews_url = URL('reviews', product_id),
        post_comment_url = URL('comment', product_id),
        post_reviews_url = URL('review', product_id),
        isAuthenticated = "true" if auth.get_user() else "false",
        product = dict(
            name=prod.name,
            seller=sellerProfile.username,
            description=prod.description,
            images=images,
            price=prod.price,
            amount=prod.amount
        )
    )

@action('comments/<product_id:int>', method=['GET'])
@action.uses(db)
def get_comments(product_id = None):
    assert product_id is not None
    data = db(db.comments.product == product_id).select()
    comments = []
    for e in data:
        dbq = db(db.userProfile.id == e.user).select()
        userProfile = dbq.first()
        comments.append({
            'username': userProfile.username,
            'text': e.text,
            'profile_pic': URL('static', 'images', 'profile', 'image1.png'),
            'profile_link': URL('profile', userProfile.username),
        })
    return dict(comments=comments)

@action('reviews/<product_id:int>', method=['GET'])
@action.uses(db)
def get_reviews(product_id = None):
    assert product_id is not None
    data = db(db.reviews.product == product_id).select()
    reviews = []
    for e in data:
        dbq = db(db.userProfile.id == e.user).select()
        userProfile = dbq.first()
        reviews.append({
            'username': userProfile.username,
            'text': e.text,
            'profile_pic': URL('static', 'images', 'profile', 'image1.png'),
            'profile_link': URL('profile', userProfile.username),
        })
    return dict(reviews=reviews)

@action('comment/<product_id:int>', method=['POST'])
@action.uses(db, auth.user)
def post_comment(product_id = None):
    assert product_id is not None
    text = request.json["comment"]
    dbq = db(db.userProfile.id == auth.user.id).select()
    userProfile = dbq.first()
    db.comments.insert(
        text=text,
        user=auth.user.id,
        product=product_id,
    )
    return "ok"

@action('review/<product_id:int>', method=['POST'])
@action.uses(db, auth.user)
def review_comment(product_id = None):
    assert product_id is not None
    text = request.json["review"]
    dbq = db(db.userProfile.id == auth.user.id).select()
    userProfile = dbq.first()
    db.reviews.insert(
        text=text,
        user=auth.user.id,
        product=product_id,
    )
    return "ok"

@action('search', method=['GET'])
@action.uses()
def search():
    q = request.params.get("q").lower()
    if len(q) < 2 or q == None:
        return dict(results=[])
    prods = db(db.products).select(db.products.ALL, orderby=db.products.name)
    results = []
    for p in prods:
        if q in p.name.lower():
            seller = db(db.userProfile.id == p.seller).select().first()
            results.append(dict(
                name=p.name,
                redirect_url=URL("product", seller.username, p.id)
            ))
    return dict(results=results)
