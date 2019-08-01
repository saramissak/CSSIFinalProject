import jinja2
import webapp2
import os

from google.appengine.api import users
from google.appengine.ext import ndb
from ClothesModel import Clothes
from CSSIUser import CssiUser


the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class AllClothes(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        # If the user is logged in...
        if user:
            upload_template = the_jinja_env.get_template('templates/all-clothes.html') #html page to be used

            clothes_query = Clothes.query()
            clothes_fetch = clothes_query.fetch()
            selected= "var_string"
            # count = "count"
            on_off = "on"

            the_variable_dict = {
                'all_clothes': clothes_fetch,
                'selected': selected,
                "on-off": on_off
            }
            self.response.write(upload_template.render(the_variable_dict))

            signout_link_html = '<a href="%s">sign out</a>' % (
                users.create_logout_url('/welcome'))
            email_address = user.nickname()
            cssi_user = CssiUser.query().filter(CssiUser.email == email_address).get()

        else:
          # If the user isn't logged in...
          login_url = users.create_login_url('/welcome')
          login_html_element = '<a href="%s">Sign in</a>' % login_url
          # Prompt the user to sign in.
          self.response.write('Please log in.<br>' + login_html_element)
