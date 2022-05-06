"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

db.define_table(
    'products',
    Field('name', requires = IS_NOT_EMPTY()),
    Field('seller', 'reference userProfile', requires = IS_NOT_EMPTY()),
    Field('description', requires = IS_NOT_EMPTY()),
    Field('image', requires = IS_NOT_EMPTY()),
    Field('price', 'float', requires = IS_FLOAT_IN_RANGE(0, 1e6)),
    Field('rating', 'decimal', requires = IS_DECIMAL_IN_RANGE(0, 5)),
    Field('amount', 'int', requires = IS_INT_IN_RANGE(1, 1e6)),
)

db.commit()


