import jinja2
import webapp2
import os

from ClothesModel import Clothes


the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


    make handlers for each article of select_clothing_piece
