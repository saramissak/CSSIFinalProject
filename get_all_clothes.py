import jinja2
import webapp2
import os
import time

from google.appengine.api import users
from google.appengine.ext import ndb
from ClothesModel import Clothes, Outfit
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
            # Clothes[selected].key.delete()
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

class ViewMadeFits(webapp2.RequestHandler):
    # def get(self):
    #     made_template = the_jinja_env.get_template('templates/made-fits-view.html') #html page to be used
    #     self.response.write(made_template.render())

    def get(self):
        user = users.get_current_user()
        # If the user is logged in...
        if user:
            made_template = the_jinja_env.get_template('templates/made-fits-view.html') #html page to be used

            outfit_query = Outfit.query().filter(Outfit.user == user.email())
            outfit_fetch = outfit_query.fetch()
            outfits = []
            for outfit in outfit_fetch:
                dict = {}
                if outfit.top:
                    dict['top'] = outfit.top.get()
                if outfit.bottoms:
                    dict['bottoms'] = outfit.bottoms.get()
                if outfit.shoes:
                    dict['shoes'] = outfit.shoes.get()
                if outfit.outerwear:
                    dict['outerwear'] = outfit.outerwear.get()
                outfits.append(dict)
            print("Printing outfit #1")
            for key in outfits[0]:
                print(outfits[0][key])
            selected= "var_string"
            # count = "count"
            on_off = "on"
            the_variable_dict = {
                "user": user,
                'all_clothes': outfits,
                'selected': selected,
                "on-off": on_off
            }
            self.response.write(made_template.render(the_variable_dict))
            # Clothes[selected].key.delete()
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
            key_to_delete = Outfit.query().filter(Outfit.number == int(to_delete)).fetch()[0].key
            Delete = key_to_delete.delete()
            time.sleep(.1)
            self.redirect('/view-made-fits')
        else:
            made_template = the_jinja_env.get_template('templates/made-fits-view.html') #html page to be used

            Outfit_query = Outfit.query().filter(Outfit.user == user.email())
            Outfit_fetch = Outfit_query.fetch()
            selected= "var_string"
            # count = "count"
            on_off = "on"
            the_variable_dict = {
                "user": user,
                'all_clothes': Outfit_fetch,
                'selected': selected,
                "on-off": on_off
            }
            self.response.write(made_template.render(the_variable_dict))
