import jinja2
import webapp2
import os
import time

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

            clothes_query = Clothes.query().filter(Clothes.user == user.email())
            clothes_fetch = clothes_query.fetch()
            selected= "var_string"
            # count = "count"
            on_off = "on"

            the_variable_dict = {
                "user": user,
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
            self.redirect(login_url)          #SIgn in HTML

    def post(self):
        user = users.get_current_user()

        if self.request.get("to_delete") != "":
            to_delete = self.request.get("to_delete")
            key_to_delete = Clothes.query().filter(Clothes.number == int(to_delete)).fetch()[0].key
            Delete = key_to_delete.delete()
            time.sleep(.1)
            self.redirect('/all_clothes')
        else:
            upload_template = the_jinja_env.get_template('templates/all-clothes.html') #html page to be used

            clothes_query = Clothes.query().filter(Clothes.user == user.email())
            clothes_fetch = clothes_query.fetch()
            selected= "var_string"
            # count = "count"
            on_off = "on"
            upload_template = the_jinja_env.get_template('templates/all-clothes.html') #html page to be used
            the_variable_dict = {
                "user": user,
                'all_clothes': clothes_fetch,
                'selected': selected,
                "on-off": on_off
            }
            self.response.write(upload_template.render(the_variable_dict))
