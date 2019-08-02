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
    user = ndb.StringProperty(required = True)

class Outfit(ndb.Model):
    top = ndb.KeyProperty(required = False)
    bottoms = ndb.KeyProperty(required = False)
    shoes = ndb.KeyProperty(required = False)
    outerwear = ndb.KeyProperty(required = False)
    user = ndb.StringProperty(required = True)

    def to_dict(self):
        result = {}
        result["img_url"] = self.img_url
        return result

class ourPics(ndb.Model):
    img = ndb.StringProperty(required = False)
