from google.appengine.ext import ndb
import webapp2
import os



class Clothes(ndb.Model):
    img_url = ndb.StringProperty(required = True)
    article_name = ndb.StringProperty(required = True)
    article_description = ndb.StringProperty(required = False)
    personal_organization = ndb.StringProperty(required = False)
    categories = ndb.StringProperty(required = False)
    number = ndb.IntegerProperty(required = True)
