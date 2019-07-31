#TO DO:
#make a function that takes you from make fits page to all clothes page,
#then pick item that take user back to fits page now With the item there

import jinja2
import webapp2
import os

from ClothesModel import Clothes
from google.appengine.api import urlfetch
import json

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def select_clothing_piece():
    make_outfits = Clothes.query(projection=[Clothes.categories], distinct=True)
    make_outfits_fetch = make_outfits.fetch()
    outfit_list = []
    for item in make_outfits_fetch:
        outfit_list.append(item.categories)
    return outfit_list

def get_shirts():
    clothing_query = Clothes.query()
    clothing_fetch = clothing_query.fetch()
    shirt_list = []
    for clothes in clothing_fetch:
        if clothes.categories == "shirt":
            shirt_list.append(clothes)
    print(shirt_list)
    return shirt_list


class FitsPage(webapp2.RequestHandler):
    def get(self):
        # This template uses jQuery, which simplifies JavaScript DOM manipulation
        make_fits_template = the_jinja_env.get_template('templates/make-fits.html')
        self.response.write(make_fits_template.render())

class ShirtsJSON(webapp2.RequestHandler):
    def get(self):
        shirts_list = get_shirts()
        objects_list = [shirt.to_dict() for shirt in shirts_list]
        self.response.write(json.dumps(objects_list))
