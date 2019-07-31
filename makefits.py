#TO DO:
#make a function that takes you from make fits page to all clothes page,
#then pick item that take user back to fits page now With the item there

import jinja2
import webapp2
import os

from CSSIUser import CssiUser
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
    clothing_fetch = clothing_query.filter(Clothes.categories == "shirt").fetch()
    shirt_list = []
    for each in clothing_fetch:
        shirt_list.append(each.img_url)
    print(shirt_list)
    print(clothing_fetch)
    return shirt_list

def get_pants():
    clothing_query = Clothes.query()
    clothing_fetch = clothing_query.filter(Clothes.categories == "pants").fetch()
    pant_list = []
    for each in clothing_fetch:
        pant_list.append(each.img_url)
    print(pant_list)
    print(clothing_fetch)
    return pant_list

def get_shoes():
    clothing_query = Clothes.query()
    clothing_fetch = clothing_query.filter(Clothes.categories == "shoes"or"sneakers").fetch()
    shoes_list = []
    for each in clothing_fetch:
        shoes_list.append(each.img_url)
    print(shoes_list)
    print(clothing_fetch)
    return shoes_list

def get_jacket():
    clothing_query = Clothes.query()
    clothing_fetch = clothing_query.filter(Clothes.categories == "jacket").fetch()
    jacket_list = []
    for each in clothing_fetch:
        jacket_list.append(each.img_url)
    print(jacket_list)
    print(clothing_fetch)
    return jacket_list

# class FitsPage(webapp2.RequestHandler):
#     def get(self):
#         # This template uses jQuery, which simplifies JavaScript DOM manipulation
#         make_fits_template = the_jinja_env.get_template('templates/make-fits.html')
#         self.response.write(make_fits_template.render())

# class ShirtsJSON(webapp2.RequestHandler):
#     def get(self):
#         shirts_list = get_shirts()
#         objects_list = [shirt.to_dict() for shirt in shirts_list]
#         list_of_shirts = []
#         for i in shirt.to_dict():
#             print(list_of_shirts.append(i))
#         jinja_dict = {
#             'shirts': list_of_shirts
#         }
#         self.response.write(json.dumps(objects_list))
