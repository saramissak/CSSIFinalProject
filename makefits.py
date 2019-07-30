#TO DO:
#make a function that takes you from make fits page to all clothes page,
#then pick item that take user back to fits page now With the item there

import jinja2
import webapp2
import os

from ClothesModel import Clothes

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
