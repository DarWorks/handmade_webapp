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

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email

url_signer = URLSigner(session)

@action('index')
@action.uses('index.html', db, auth)
def index():
    return dict(
        # COMPLETE: return here any signed URLs you need.
        my_callback_url = URL('my_callback', signer=url_signer),
    )

@action('product/<seller_name>/<product_id:int>')
@action.uses('product.html')
def product(seller_name=None, product_id=None):
    assert product_id is not None
    assert seller_name is not None
    # TODO: grab product data from DB using product id and confirm that seller name matches
    # Then serialize the data in the format that is used in the html template like shown below
    return dict(
        product = dict(
            name="Product Name",
            seller="SellerUsername",
            description="This is the product description. ",
            images=("images/product/image1.png", "images/product/image2.png")
        ),
        thoughts=(
            dict(
                username="Username1",
                comment="This is my thought",
                profile_pic="images/profile/image1.png"
            ),
            dict(
                username="Username2",
                comment="This is my second thought",
                profile_pic="images/profile/image2.jpg"
            )
        ),
        reviews=(
            dict(
                username="Username1",
                comment="This is my review",
                profile_pic="images/profile/image1.png"
            ),
            dict(
                username="Username2",
                comment="This is my second review",
                profile_pic="images/profile/image2.jpg"
            )
        ),
    )
