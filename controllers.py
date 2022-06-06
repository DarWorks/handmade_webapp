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

import datetime
import json
import os
import stripe
import random
from functools import reduce

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email
from .models import get_user_FirstName
from .models import get_user_LastName
from .settings import APP_FOLDER, APP_NAME

from py4web.utils.form import Form, FormStyleBulma
from py4web.utils.grid import Grid, GridClassStyleBulma

url_signer = URLSigner(session)

# Reads the stripe keys.
with open(os.path.join(APP_FOLDER, 'private', 'stripe_keys.json'), 'r') as f:
    STRIPE_KEY_INFO = json.load(f)
stripe.api_key = STRIPE_KEY_INFO['test_private_key']

def full_url(u):
    p = request.urlparts
    return p.scheme + "://" + p.netloc + u


###############################################################################

# Helper functions for the index / homepage and displaying product categories

def ratingAndNamesHelper(query):
    """
    A helper function to query the first name, last name, username, aggregate rating,
    product name (capitalise initials) , price (change in datatype)

    NOTE: for better displaying purposes, the first name and last name of the user and the product name
            have their initials capitalised using the title() function. The changes are not reflected in the database
        Same with other modifications in the function
    """
    i = 1
    for row in query:
        row["price"] = "{:.2f}".format(row["price"])
        row["name"] = row["name"].title()
        if row["ratingtotal"] == 0 or row["ratingnum"] == 0:
            row["aggegateRating"] = 0
            row["ratingPresent"] = False
        else:
            row["aggegateRating"] = row["ratingtotal"] / row["ratingnum"]
            row["ratingPresent"] = True
        sellerQuery = db(db.userProfile.id == row["sellerid"]).select()
        for seller in sellerQuery:
            row["first_name"] = seller["first_name"].title()
            row["last_name"] = seller["last_name"].title()
            row["username"] = seller["username"]
        row["queryRowID"] = i
        i += 1


def productAndSellerLinkHelper(query):
    """
       A helper function to add product link and seller link
    """
    for product in query:
        u = db(db.userProfile.id == product["sellerid"]).select().first()
        product["prodURL"] = URL("product", u["username"], product["id"])
        product["sellerURL"] = URL("profile", u["username"])


def preferencesQueryHelper(p1, p2, p3):
    """
        A helper function for quering user preferences based products
        If there are less products based on user preferences then this randomises
    """

    if (p1 == p2 == p3):
        l = p1
    elif p1 == p3:
        l = p1 + p2
    elif p1 == p2:
        l = p1 + p3
    elif p2 == p3:
        l = p1
    else:
        l = p1 + p2 + p3

    length = len(l) - 1
    if len(l) > 4:
        random_index = random.randint(4, length)
        l = l[random_index-4:random_index]
    elif len(l) < 4:
        while True:
            if len(l) == 4:
                break

            gap = 4 - len(l)

            randomProducts = db(db.products.id).select(orderby='<random>', limitby=(0, gap)).as_list()

            id_list = id_lister(l)

            unqiueRandomProducts = []
            for i in randomProducts:
                if i["id"] not in id_list:
                    unqiueRandomProducts.append(i)

            l = l + unqiueRandomProducts

    return l


def id_lister(l):
    """
        another helper function used in preferences helper
    """
    id_list = []
    for i in l:
        id_list.append(i["id"])
    return id_list

###############################################################################


#//////////////////////////////////////////////////////////
# HOMEPAGE
#//////////////////////////////////////////////////////////
@action('index')
@action.uses('index.html', db, auth, url_signer)
def index():
    # 1) queriying all users to display  DB for debugging
    # 2) querying DB to see if a user with the current email exists in the DB
    theDB = db(db.userProfile).select().as_list()
    currentUser = db(
        db.userProfile.user_email == get_user_email()).select().first()
    isPersonalized = False
    currentUserName=""

    if currentUser is not None and currentUser.username is not None:
        currentUserName= currentUser.username
        isPersonalized= currentUser.isPersonlized
    else:
        currentUserName=None
        isPersonalized = False


    # Queries for displaying products-
    newProducts = db(db.products).select(orderby=~db.products.id, limitby=(0, 4)).as_list()

    # user session variables to be used in index.html
    customerID = 0
    display = False
    firstProductRow = newProducts

    firstRowText = "New Items"


    # if no active user session set display = false
    # active session, but no DB entry --> prompt customization
    if get_user_email() == None:
        display = False
    else:
        if currentUser == None:
            isPersonalized = False
            display = True
        else:
            firstRowText = "For You"

            l1 = db(db.products.type == currentUser.preference1).select(orderby='<random>').as_list()
            l2 = db(db.products.type == currentUser.preference2).select(orderby='<random>').as_list()
            l3 = db(db.products.type == currentUser.preference3).select(orderby='<random>').as_list()

            # calls preferences query helper
            l = preferencesQueryHelper(l1, l2, l3)

            firstProductRow = l

    # calls helper function to add product link
    productAndSellerLinkHelper(firstProductRow)

    # calls helper function to query the first name, last name, username, aggregate rating, price (change in datatype)
    ratingAndNamesHelper(firstProductRow)

    # sending userSession data to conditionally render index.html
    # note, can access as currentUsers['isPersonalized'] etc.
    return dict(
        # COMPLETE: return here any signed URLs you need.
        my_callback_url=URL('my_callback', signer=url_signer),
        isPersonalized=isPersonalized,
        customerID=customerID,
        display=display,
        theDB=theDB,
        firstProductRow=firstProductRow,
        firstRowText=firstRowText,
        url_signer = url_signer,
        currentUserName =currentUserName,
        get_index_data_url=URL('get_index_data'),
    )


@action('get_index_data')
@action.uses(db, auth)
def get_index_data():

    # Queries for displaying 2nd row-
    trendingProducts = db(db.products).select(orderby='<random>', limitby=(0, 4)).as_list()

    # calls helper function to add product link
    productAndSellerLinkHelper(trendingProducts)

    # calls helper function to query the first name, last name, username, aggregate rating, price (change in datatype)
    ratingAndNamesHelper(trendingProducts)

    return dict(trendingProducts=trendingProducts)


@action('about')
@action.uses('about.html', db, auth, url_signer)
def about():

    # getting current user info for the profile/cart buttons
    theDB = db(db.userProfile).select().as_list()
    currentUser = db(
        db.userProfile.user_email == get_user_email()).select().first()
    isPersonalized = False
    currentUserName = ""

    if currentUser is not None and currentUser.username is not None:
        currentUserName = currentUser.username
        isPersonalized = currentUser.isPersonlized
    else:
        currentUserName = None
        isPersonalized = False

    return dict(isPersonalized=isPersonalized, currentUserName=currentUserName, url_signer = url_signer)


@action('faq')
@action.uses('faq.html', db, auth, url_signer)
def faq():

    # getting current user info for the profile/cart buttons
    theDB = db(db.userProfile).select().as_list()
    currentUser = db(
        db.userProfile.user_email == get_user_email()).select().first()
    isPersonalized = False
    currentUserName = ""

    if currentUser is not None and currentUser.username is not None:
        currentUserName = currentUser.username
        isPersonalized = currentUser.isPersonlized
    else:
        currentUserName = None
        isPersonalized = False

    return dict(isPersonalized=isPersonalized, currentUserName=currentUserName, url_signer = url_signer)


#//////////////////////////////////////////////////////////
# SHOPPING CART
#//////////////////////////////////////////////////////////

@action('shopping_cart')
@action.uses('shopping_cart.html', db, auth, url_signer.verify())
def shopping_cart():

    # getting current user info for the profile/cart buttons
    theDB = db(db.userProfile).select().as_list()
    currentUser = db(
        db.userProfile.user_email == get_user_email()).select().first()
    isPersonalized = False
    currentUserName = ""

    if currentUser is not None and currentUser.username is not None:
        currentUserName = currentUser.username
        isPersonalized = currentUser.isPersonlized
    else:
        currentUserName = None
        isPersonalized = False

    return dict(
            currentUserName=currentUserName,
            isPersonalized=isPersonalized,
            url_signer=url_signer,
            pay_url = URL('pay', signer=url_signer),
            stripe_key = STRIPE_KEY_INFO['test_public_key'],
            app_name = APP_NAME,
            get_product_url = URL('get_product')
        )

@action('get_product')
@action.uses(db, auth)
def get_product():
    id = request.params.get('id')

    row = db(db.products.id == id).select().first()
    return dict(row=row)

@action('pay', method="POST")
@action.uses(db, url_signer)
def pay():
    items = request.json.get('cart')
    fulfillment = request.json.get('fulfillment')

    line_items = []
    item_names = []
    for it in items:
        p = db.products(it['id'])

        line_item = {
                'quantity': 1,
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(p.price * 100),
                    'product_data': {
                        'name': p.name,
                    }
                }
        }

        line_items.append(line_item)
        item_names.append(p.name)

    order_id = db.customer_order.insert(
        ordered_items= item_names,
        fulfillment=json.dumps(fulfillment),
    )

    stripe_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=full_url(URL('successful_payment', order_id)),
        cancel_url=full_url(URL('cancelled_payment', order_id)),
    )
    return dict(ok=True, session_id=stripe_session.id)

@action('successful_payment/<order_id:int>')
@action.uses('successful_payment.html', db, auth, url_signer)
def successful_payment(order_id=None):
    order = db(db.customer_order.id == int(order_id)).select().first()
    if order is None:
        redirect(URL('index'))
    order.paid = True
    order.paid_on = datetime.datetime.utcnow()
    order.update_record()

    fulfillment = json.loads(order.fulfillment)
    return dict(name=fulfillment["name"], address=fulfillment["address"], app_name = APP_NAME, url_signer=url_signer)

@action('cancelled_payment/<order_id:int>')
@action.uses(db, auth)
def cancelled_payment(order_id=None):
    try:
        db(db.customer_order.id == int(order_id)).delete()
    except:
        pass
    redirect(URL('index'))

@action('view_orders')
@action('view_orders/<path:path>', method=['POST', 'GET'])
@action.uses('view_order.html', db, auth, session, url_signer.verify())
def view_orders(path=None):

    # getting current user info for the profile/cart buttons
    theDB = db(db.userProfile).select().as_list()
    currentUser = db(
        db.userProfile.user_email == get_user_email()).select().first()
    isPersonalized = False
    currentUserName = ""

    if currentUser is not None and currentUser.username is not None:
        currentUserName = currentUser.username
        isPersonalized = currentUser.isPersonlized
    else:
        currentUserName = None
        isPersonalized = False


    grid = Grid(path,
                query= db.customer_order.id > 0,
                editable=False, deletable=False, details=False, create=False,
                grid_class_style=GridClassStyleBulma,
                formstyle=FormStyleBulma,
                )
    return dict(grid=grid, isPersonalized=isPersonalized, currentUserName=currentUserName, url_signer=url_signer)


@action('edit_product/<product_id:int>', method=['GET'])
@action.uses('edit_product.html', db, auth.user, session, url_signer)
def edit_product_page(product_id=None):
    assert product_id is not None
    data = db(db.products.id == product_id).select().first()
    user = db(db.userProfile.user_email == get_user_email()).select().first()
    if (data is None):
        return "not found"
    if (user is None) or (data.sellerid != user.id):
        return "unauthorized"
    return dict(
        product_id=data.id,
        product_name=data.name,
        type=data.type if data.type is not None else "",
        description=data.description,
        price=data.price,
        add_product_info_url = URL('edit_product_info', user.username, data.id, signer=url_signer),
        username=user.username,
        url_signer=url_signer,
        delete_prod_url=URL('delete_product', data.id, signer=url_signer),
        on_delete_url = URL('profile', user.username),
        on_edit_url = URL('product', user.username, data.id),
    )

@action('edit_product_info/<username>/<product_id:int>', method=['POST'])
@action.uses(db, auth.user, url_signer.verify())
def add_product_info(product_id=None, username=None):
    db(db.products.id == product_id).update(
        name=request.json.get('product_name'),
        type=request.json.get('product_type'),
        description=request.json.get('product_description'),
        price=request.json.get('product_price'),
    )
    image1=request.json.get('product_image1')
    image2=request.json.get('product_image2')
    image3=request.json.get('product_image3')
    image4=request.json.get('product_image4')
    if len(image1) > 0:
        db(db.products.id == product_id).update(
            image1=image1,
            image2=image2,
            image3=image3,
            image4=image4,
        )
    return "ok"

@action('delete_product/<product_id:int>', method=['POST'])
@action.uses(db, auth.user, session, url_signer.verify())
def delete_product(product_id=None):
    try:
        db(db.products.id == product_id).delete()
    except:
        pass
    return "ok"

#//////////////////////////////////////////////////////////
# PROFILE PAGE
#//////////////////////////////////////////////////////////

@action('profile/<username>')
@action.uses('profile.html', auth)
def profile(username=None):

    # getting current user info for the profile/cart buttons
    theDB = db(db.userProfile).select().as_list()
    currentUser = db(
        db.userProfile.user_email == get_user_email()).select().first()
    isPersonalized = False
    currentUserName = ""

    if currentUser is not None and currentUser.username is not None:
        currentUserName = currentUser.username
        isPersonalized = currentUser.isPersonlized
    else:
        currentUserName = None
        isPersonalized = False

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
        image=x["image1"],
        editURL=URL('edit_product', x["id"]),
    ), db(db.products.sellerid == userProfile.id).select().as_list())
    return dict(
        isPersonalized =isPersonalized,
        currentUserName=currentUserName,
        url_signer=url_signer,
        my_callback_url = URL('my_callback', signer=url_signer),
        isAccountOwner = isAccountOwner,
        profile = dict(
            username= username,
            profile_pic= "images/profile/default.jpg"
        ),
        selling = selling,
        purchased = []
    )

@action('add_product/<username>')
@action.uses('add_product.html', db, auth, url_signer.verify())
def add_product(username=None):
    assert username is not None
    return dict(
        add_product_info_url = URL('add_product_info', username),
        username=username,
        url_signer=url_signer,
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

    return dict(username=username, url_signer=url_signer,)


#//////////////////////////////////////////////////////////
# PRODUCT PAGE
#//////////////////////////////////////////////////////////

@action('product/<username>/<product_id:int>')
@action.uses('product.html', auth, url_signer)
def product(username=None, product_id=None):

    # getting current user info for the profile/cart buttons
    theDB = db(db.userProfile).select().as_list()
    currentUser = db(
        db.userProfile.user_email == get_user_email()).select().first()
    isPersonalized = False
    currentUserName = ""

    if currentUser is not None and currentUser.username is not None:
        currentUserName = currentUser.username
        isPersonalized = currentUser.isPersonlized
    else:
        currentUserName = None
        isPersonalized = False


    assert product_id is not None
    assert username is not None
    data = db(db.products.id == product_id).select()
    prod = data.first()
    if prod is None:
        return "404 Not found"
    data = db(db.userProfile.id == prod.sellerid).select()
    sellerProfile = data.first()
    if sellerProfile is None or sellerProfile.username != username:
        return "404 Not found"
    images = []
    if prod.image1 is not None:
        images.append({"id":1, "src": prod.image1})
    if prod.image2 is not None and len(prod.image2) > 0:
        images.append({"id":2, "src":prod.image2})
    if prod.image3 is not None and len(prod.image3) > 0:
        images.append({"id":3, "src":prod.image3})
    if prod.image4 is not None and len(prod.image4) > 0:
        images.append({"id":4, "src":prod.image4})
    # check if user has username
    hasUsername = False
    ausername = ""
    if auth.get_user():
        u = db(db.userProfile.user_email == get_user_email()).select().first()
        hasUsername = (u is not None) and (u.username is not None) and (len(u.username) > 0)
        if hasUsername:
            ausername = u.username
    # check if user has purchased this before to allow them to review the item
    hasPurchasedBefore = False

    if (prod.ratingnum == 0):
        existrating = False
        avgrating = 0
    else:
        existrating = True
        avgrating = prod.ratingtotal / prod.ratingnum

    return dict(
        isPersonalized =isPersonalized,
        currentUserName =currentUserName,
        url_signer=url_signer,
        app_name = APP_NAME,
        get_product_url = URL('get_product'),
        product_id=product_id,
        login_url= URL("auth", "login"),
        personalization_url=URL("add_user_personalization"),
        get_comments_url = URL('comments', product_id),
        get_reviews_url = URL('reviews', product_id),
        post_comment_url = URL('comment', product_id),
        post_reviews_url = URL('review', product_id),
        set_rating_url = URL('set_rating', ausername, product_id, signer=url_signer),
        get_rating_url = URL('get_rating', ausername, product_id, signer=url_signer),
        isAuthenticated = "true" if auth.get_user() else "false",
        hasUsername= "true" if hasUsername else "false",
        hasPurchasedBefore="true" if hasPurchasedBefore else "false",
        avgrating=avgrating,
        existrating=existrating,
        product = dict(
            name=prod.name,
            seller=sellerProfile.username,
            description=prod.description,
            images=images,
            price=prod.price,
            amount=prod.amount,
        )
    )

@action('get_rating/<username>/<product_id:int>')
@action.uses(db)
def rating(username=None, product_id=None):
    assert product_id is not None

    user = db(db.userProfile.username == username).select().first()
    data = db((db.ratingvals.product_id == product_id) & (db.ratingvals.rater == user.id)).select().first()

    if (data == None):
        return dict(rating=0)

    return dict(rating=data.rating)

@action('set_rating/<username>/<product_id:int>', method=['POST'])
@action.uses(db)
def set_rating(username=None, product_id=None):
    assert product_id is not None

    user = db(db.userProfile.username == username).select().first()
    data = db((db.ratingvals.product_id == product_id) & (db.ratingvals.rater == user.id)).select().first()

    if (data == None):
        db.ratingvals.insert(
            product_id=product_id,
            rating=request.json.get('rating'),
            rater=user.id,
        )
        database = db(db.products.id == product_id).select().first()
        total = database.ratingtotal
        num = database.ratingnum
        db(db.products.id == product_id).update(ratingtotal = total + request.json.get('rating'), ratingnum = num + 1)

    else:
        storage = data.rating
        db((db.ratingvals.product_id == product_id) & (db.ratingvals.rater == user.id)).update(rating = request.json.get('rating'))
        database = db(db.products.id == product_id).select().first()
        total = database.ratingtotal
        db(db.products.id == product_id).update(ratingtotal = total - storage + request.json.get('rating'))

    return dict()

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
    redirectReason = request.params.get("reason")
    return dict(
        #signed? URL for the callbacks
        add_personalization_url = URL('add_personalization_info'),
        load_users_url = URL('load_users', signer=url_signer),
        email = email,
        reason = redirectReason,
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


#//////////////////////////////////////////////////////////
# PRODUCT CATEGORIES-
#//////////////////////////////////////////////////////////


@action('display_product_category/<product_type>')
@action.uses('display_product_category.html', db, auth, url_signer)
def display_product_category(product_type=None):
    assert product_type is not None

    # getting current user info for the profile/cart buttons
    theDB = db(db.userProfile).select().as_list()
    currentUser = db(
        db.userProfile.user_email == get_user_email()).select().first()
    isPersonalized = False
    currentUserName = ""

    if currentUser is not None and currentUser.username is not None:
        currentUserName = currentUser.username
        isPersonalized = currentUser.isPersonlized
    else:
        currentUserName = None
        isPersonalized = False

    return dict(product_type=product_type,
                isPersonalized=isPersonalized,
                currentUserName=currentUserName,
                url_signer=url_signer,
                get_product_category_data_url=URL('get_product_category_data'),
                )


@action('get_product_category_data')
@action.uses(db, auth)
def get_product_category_data():
    product_type = request.params.get("product_type")
    rows = db(db.products.type == product_type).select().as_list()

    # calls helper functions to add product link
    # and query the first name, last name, username, aggregate rating, price (change in datatype)
    ratingAndNamesHelper(rows)
    productAndSellerLinkHelper(rows)

    return dict(rows=rows)


#//////////////////////////////////////////////////////////
# Layout PAGE
#//////////////////////////////////////////////////////////

@action('layoutUrls')
@action.uses('layout.html', db, auth, url_signer)
def layoutUrlSigner():
    return dict(
        # COMPLETE: return here any signed URLs you need.
        url_signer=url_signer,

    )
