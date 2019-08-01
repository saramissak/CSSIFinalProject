from google.appengine.ext import ndb
import webapp2
import os

from CSSIUser import CssiUser

class Clothes(ndb.Model):
    img_url = ndb.StringProperty(required = True)
    article_name = ndb.StringProperty(required = True)
    article_description = ndb.StringProperty(required = False)
    personal_organization = ndb.StringProperty(required = False)
    categories = ndb.StringProperty(required = False)
    number = ndb.IntegerProperty(required = True)

class outfit(ndb.Model):
<<<<<<< HEAD
    top = ndb.StringProperty(required = True)
    bottoms = ndb.StringProperty(required = True)
    shoes = ndb.StringProperty(required = True)
    outerwear = ndb.StringProperty(required = True)
=======
    top=ndb.StringProperty(required = False)
    bottoms=ndb.StringProperty(required = False)
    shoes=ndb.StringProperty(required = False)
    outerwear=ndb.StringProperty(required = False)
>>>>>>> 580b062dda853ab2de9e5a472564095b43895cf6

    def to_dict(self):
        result = {}
        result["img_url"] = self.img_url
        return result
