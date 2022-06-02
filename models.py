"""
This file defines the database models
"""

from __future__ import unicode_literals
import datetime
# from importlib.metadata import requires

from pkg_resources import require
from .common import db, Field, auth
from pydal.validators import *

def get_user_id():
    return auth.current_user.get("id") if auth.current_user else None
def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None
def get_user_FirstName():
    return auth.current_user.get('first_name') if auth.current_user else None
def get_user_LastName():
    return auth.current_user.get('last_name') if auth.current_user else None
def get_time():
    return datetime.datetime.utcnow()



db.define_table(
    'userProfile',
    Field('first_name', 'text', default="", requires=IS_NOT_EMPTY()),
    Field('last_name', 'text', default="", requires=IS_NOT_EMPTY()),
    Field('user_email', default=get_user_email, requires=IS_NOT_EMPTY()),
    Field('username', 'text', unique=True, requires=IS_NOT_EMPTY()),  # 1* Check comments below for details w.r to 'uniqie' attribute
    Field('balance', 'float', default=0, requires=IS_FLOAT_IN_RANGE(0, 1e6)), # 2* Check below
    Field('isPersonlized', 'boolean', default=False),
    Field('preference1', 'text', default=""),
    Field('preference2', 'text', default=""),
    Field('preference3', 'text', default=""),

)

db.userProfile.username.requires = (IS_NOT_IN_DB(db, 'userProfile.username'))
db.userProfile.id.readable = db.userProfile.id.writable = False

db.define_table(
    'products',
    Field('name', requires = IS_NOT_EMPTY()),
    # Removed for testing, uncomment when userprofile complete
    Field('sellerid', 'reference userProfile', requires = IS_NOT_EMPTY()),
    Field('type'),
    Field('description', requires = IS_NOT_EMPTY()),
    Field('image1', requires=IS_NOT_EMPTY(), default=""),
    Field('image2'),
    Field('image3'),
    Field('image4'),
    Field('price', 'float', requires = IS_FLOAT_IN_RANGE(0.5, 1e6)),
    Field('rating', 'float', requires = IS_FLOAT_IN_RANGE(0, 1e6)),
    Field('ratingtotal', 'float', default=0),
    Field('ratingnum', 'float', default=0),
    Field('amount', 'float', default=1, requires = IS_FLOAT_IN_RANGE(0, 1e6)),
)

db.define_table('customer_order',
    Field('user_email', default=get_user_email, requires=IS_NOT_EMPTY()),
    Field('order_date', default=get_time),
    Field('ordered_items', 'text'),
    Field('ordered_items_ids', 'text'),
    Field('fulfillment', 'text'),
    Field('paid', 'boolean', default=False),
    Field('created_on', 'datetime', default=get_time),
    Field('paid_on', 'datetime'),
)

db.define_table(
    'comments',
    Field('user', 'reference userProfile', requires=IS_NOT_EMPTY()),
    Field('product', 'reference products', require=IS_NOT_EMPTY()),
    Field('text', requires=IS_NOT_EMPTY())
)

db.define_table(
    'order_history',
    Field('sellerid', 'integer', requires=IS_NOT_EMPTY()),
    Field('buyerid', 'integer', requires=IS_NOT_EMPTY()),
    Field('productid', 'integer', requires=IS_NOT_EMPTY()),
)

db.define_table(
    'ratingvals',
    Field('product_id', 'reference products'),
    Field('rating', 'integer', default=0),
    Field('rater', 'reference userProfile', requires=IS_NOT_EMPTY()),
)

db.define_table(
    'reviews',
    Field('user', 'reference userProfile', requires=IS_NOT_EMPTY()),
    Field('product', 'reference products', require=IS_NOT_EMPTY()),
    Field('text', requires=IS_NOT_EMPTY())
)

db.commit()
