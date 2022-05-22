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
from .models import get_user_FirstName
from .models import get_user_LastName
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
@action('index')
@action.uses('index.html', db, auth, url_signer)
def index():
    # 1) queriying all users to display  DB for debugging
    # 2) querying DB to see if a user with the currect email exists in the DB
    theDB = db(db.userProfile).select().as_list()
    currentUser = db(
        db.userProfile.user_email == get_user_email()).select().first()

    # user session variables to be used in index.html
    customerID = 0
    isPersonalized = False
    display = False

    # if no active user session set display = false
    # active session, but no DB entry --> prompt customization
    if get_user_email() == None:
        display = False
    else:
        if currentUser == None:
            isPersonalized = False
            display = True

    # sending userSession data to conditionally render index.html
    # note, can access as currentUsers['isPersonalized'] etc.
    return dict(
        # COMPLETE: return here any signed URLs you need.
        my_callback_url=URL('my_callback', signer=url_signer),
        isPersonalized=isPersonalized,
        customerID=customerID,
        display=display,
        theDB=theDB,
    )


@action('about')
@action.uses('about.html', db, auth, url_signer)
def about():
    return dict()


@action('faq')
@action.uses('faq.html', db, auth, url_signer)
def faq():
    return dict()


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
    userProfile = db(db.userProfile.username == username).select().first()
    if userProfile is None:
        return "404 profile not found"
    isAccountOwner = False
    # check if this person is the account owner to display currency
    if user is not None:
        u = db(db.userProfile.user_email == get_user_email()).select().first()
        if u is not None and u.username == username:
            isAccountOwner = True
    selling = map(lambda x: dict(
        id=x["id"],
        seller=db(db.userProfile.id==x["sellerid"]).select().first().username,
        image=x["image1"]
    ), db(db.products.sellerid == userProfile.id).select().as_list())
    return dict(
        my_callback_url = URL('my_callback', signer=url_signer),
        isAccountOwner = isAccountOwner,
        profile = dict(
            username= username,
            total_credits=userProfile.balance,
            profile_pic= "images/profile/default.jpg"
        ),
        selling = selling,
        purchased = []
    )

@action('add_product/<username>')
@action.uses('add_product.html', db, auth, url_signer)
def add_product(username=None):
    assert username is not None
    return dict(
        add_product_info_url = URL('add_product_info', username),
        username=username,
    )

@action('add_product_info/<username>', method=['POST'])
@action.uses(db, auth.user)
def add_product_info(username=None):
    assert username is not None
    seller = db(db.userProfile.username == username).select().first()
    id = db.products.insert(
        name=request.json.get('product_name'),
        sellerid=seller.id,
        type=request.json.get('product_type'),
        description=request.json.get('product_description'),
        price=request.json.get('product_price'),
        image1=request.json.get('product_image1'),
    )

    return dict(username=username)


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
    data = db(db.userProfile.id == prod.sellerid).select()
    sellerProfile = data.first()
    if sellerProfile is None or sellerProfile.username != seller_name:
        return "404 Not found"
    images = []
    if prod.image1 is not None:
        images.append({"id":1, "src": prod.image1})
    if prod.image2 is not None:
        images.append({"id":2, "src":prod.image2})
    if prod.image3 is not None:
        images.append({"id":3, "src":prod.image3})
    if prod.image4 is not None:
        images.append({"id":4, "src":prod.image4})
    # check if user has username
    hasUsername = False
    if auth.get_user():
        u = db(db.userProfile.user_email == get_user_email()).select().first()
        hasUsername = (u is not None) and (u.username is not None) and (len(u.username) > 0)
    return dict(
        my_callback_url = URL('my_callback', signer=url_signer),
        get_comments_url = URL('comments', product_id),
        get_reviews_url = URL('reviews', product_id),
        post_comment_url = URL('comment', product_id),
        post_reviews_url = URL('review', product_id),
        isAuthenticated = "true" if auth.get_user() else "false",
        hasUsername= "true" if hasUsername else "false",
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
            'profile_pic': URL('static', 'images', 'profile', 'default.jpg'),
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
            'profile_pic': URL('static', 'images', 'profile', 'default.jpg'),
            'profile_link': URL('profile', userProfile.username),
        })
    return dict(reviews=reviews)

@action('comment/<product_id:int>', method=['POST'])
@action.uses(db, auth.user)
def post_comment(product_id = None):
    assert product_id is not None
    text = request.json["comment"]
    userProfile = db(db.userProfile.user_email == get_user_email()).select().first()
    db.comments.insert(
        text=text,
        user=userProfile.id,
        product=product_id,
    )
    return "ok"

@action('review/<product_id:int>', method=['POST'])
@action.uses(db, auth.user)
def review_comment(product_id = None):
    assert product_id is not None
    text = request.json["review"]
    userProfile = db(db.userProfile.user_email == get_user_email()).select().first()
    db.reviews.insert(
        text=text,
        user=userProfile.id,
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
            seller = db(db.userProfile.id == p.sellerid).select().first()
            results.append(dict(
                name=p.name,
                redirect_url=URL("product", seller.username, p.id)
            ))
    return dict(results=results)

@action('username', method=['GET'])
@action.uses(db, auth.user)
def getUsername():
    userProfile = db(db.userProfile.user_email == get_user_email()).select().first()
    if userProfile is not None and userProfile.username is not None:
        return dict(username=userProfile.username)
    return dict(username="")

#//////////////////////////////////////////////////////////
# PERSONALIZATION PAGE
#//////////////////////////////////////////////////////////


@action('add_user_personalization')
@action.uses('personalization.html', db, auth, url_signer)
def add_personalization():
    email = get_user_email()

    return dict(
        #signed? URL for the callbacks
        add_personalization_url = URL('add_personalization_info'),
        load_users_url = URL('load_users', signer=url_signer),
        email = email,

    )


#todo: define add_personalisation_info function
@action('add_personalization_info', method=['POST'])
@action.uses(db, auth )
def add_personalization_info():

    # Current user session details to insert into DB
    email = get_user_email()
    firstName = get_user_FirstName()
    lastName = get_user_LastName()


    # inserting into DB & storing id to be returned as dictionary
    id = db.userProfile.insert(
        first_name= firstName,
        last_name= lastName,
        user_email= email,
        username= request.json.get('user_userName'),
        preference1= request.json.get('user_preference1'),
        preference2= request.json.get('user_preference2'),
        preference3= request.json.get('user_preference3'),
        balance= 0.0,
        isPersonlized= True,
    )


    return dict(id =id)


# API function to retrieve users in DB =>debuggin purposes for now
@action('load_users')
@action.uses(url_signer.verify(), db)
def load_users():
    rows = db(db.userProfile).select().as_list()
    return dict(rows=rows)


# PRODUCT CATEGORIES-

@action('display_category_1')
@action.uses('display_category_1.html', db)
def display_category_1():
    rows = db(db.products.type == "Jewelry & Accessories").select().as_list()
    #x = rows[0]
    #y = x['type']
    return dict(rows=rows)


@action('display_category_2')
@action.uses('display_category_2.html', db)
def display_category_2():
    rows = db(db.products.type == "Clothing & Shoes").select().as_list()
    return dict(rows=rows)


@action('display_category_3')
@action.uses('display_category_3.html', db)
def display_category_3():
    rows = db(db.products.type == "Home & Living").select().as_list()
    return dict(rows=rows)


@action('display_category_4')
@action.uses('display_category_4.html', db)
def display_category_4():
    rows = db(db.products.type == "Toys & Entertainment").select().as_list()
    return dict(rows=rows)


@action('display_category_5')
@action.uses('display_category_5.html', db)
def display_category_5():
    rows = db(db.products.type == "Art & Collectibles").select().as_list()
    return dict(rows=rows)


@action('display_category_6')
@action.uses('display_category_6.html', db)
def display_category_6():
    rows = db(db.products.type == "Other").select().as_list()
    return dict(rows=rows)

