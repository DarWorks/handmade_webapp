"""
This file defines the database models
"""

from __future__ import unicode_literals
import datetime
# from importlib.metadata import requires

from pkg_resources import require
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_user_FirstName():
    return auth.current_user.get('first_name') if auth.current_user else None
def get_user_LastName():
    return auth.current_user.get('last_name') if auth.current_user else None




def get_time():
    return datetime.datetime.utcnow()


# userProfile DB table
db.define_table(
    'userProfile',
    Field('first_name','text',default="", requires=IS_NOT_EMPTY()),
    Field('last_name','text',default="", requires=IS_NOT_EMPTY()),
    Field('user_email', default=get_user_email, requires=IS_NOT_EMPTY()),
    Field('username','text', unique=True, requires=IS_NOT_EMPTY()),  # 1* Check comments below for details w.r to 'uniqie' attribute
    Field('balance','float', default=0, requires=IS_FLOAT_IN_RANGE(0, 1e6)), # 2* Check below
    Field('isPersonlized','boolean', default=False),
    Field('preference1', 'text', default=""),
    Field('preference2', 'text', default=""),
    Field('preference3', 'text', default=""),
    # Field('user_email', default=get_user_email),

)
# 1* unique=TRUE ensures the field entry is unique, but does not display an error prompt within implemented forms
# the error prompt is implemented here:
db.userProfile.username.requires= (IS_NOT_IN_DB(db, 'userProfile.username'))
# Not 100% sure if this is the correct argument syntax for validating unique username in the DB, but
# it will become obvious when implementing the respective form.
#src: https://www.web2pyref.com/reference/is_not_in_db-validator


# 2* kinda just tossed this in here, are we going to attribute this here or in a potential,
# connected 'wallet' DB table? LMK




# making the userProfile id read/write inaccessible to user
db.userProfile.id.readable = db.userProfile.id.writable = False



### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

db.define_table(
    'products',
    Field('name', requires = IS_NOT_EMPTY()),
    # Removed for testing, uncomment when userprofile complete
    # Field('seller', 'reference userProfile', requires = IS_NOT_EMPTY()),
    Field('type'),
    Field('description', requires = IS_NOT_EMPTY()),
    Field('image1'),
    Field('image2'),
    Field('image3'),
    Field('image4'),
    Field('price', 'float', requires = IS_FLOAT_IN_RANGE(0.5, 1e6)),
    Field('rating', 'float', requires = IS_FLOAT_IN_RANGE(0, 1e6)),
    Field('amount', 'float', requires = IS_FLOAT_IN_RANGE(0, 1e6)),
)

db.define_table(
    'comments',
    Field('user', 'reference userProfile', requires=IS_NOT_EMPTY()),
    Field('product', 'reference products', require=IS_NOT_EMPTY()),
    Field('text', requires=IS_NOT_EMPTY())
)

db.define_table(
    'reviews',
    Field('user', 'reference userProfile', requires=IS_NOT_EMPTY()),
    Field('product', 'reference products', require=IS_NOT_EMPTY()),
    Field('text', requires=IS_NOT_EMPTY())
)

db.commit()
