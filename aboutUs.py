import jinja2
import webapp2
import os

from ClothesModel import Clothes


the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class about(webapp2.RequestHandler):
    def get(self):
        aboutus_template = the_jinja_env.get_template('templates/aboutus.html') #html page to be used
        self.response.write(aboutus_template.render())
