import webapp2
import jinja2
import os
import json

from makefits import get_shirts
from makefits import get_pants
from makefits import get_jacket
from makefits import get_shoes
from Search import search
from aboutUs import about
from aboutUs import welcome
from ClothesModel import Clothes
from Upload import Upload
from get_all_clothes import AllClothes
from makefits import select_clothing_piece
# from makefits import ShirtsJSON


from google.appengine.api import users
from google.appengine.ext import ndb

jinja_current_dir = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class CssiUser(ndb.Model):
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()
  email = ndb.StringProperty()

class MainHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    # If the user is logged in...
    if user:
      signout_link_html = '<a href="%s">sign out</a>' % (
          users.create_logout_url('/'))
      email_address = user.nickname()
      cssi_user = CssiUser.query().filter(CssiUser.email == email_address).get()
      # If the user is registered...
      if cssi_user:
        # Greet them with their personal information
        self.response.write('''
            Welcome %s %s (%s)! <br> %s <br>''' % (
              cssi_user.first_name,
              cssi_user.last_name,
              email_address,
              signout_link_html))
      # If the user isn't registered...
      else:
        # Offer a registration form for a first-time visitor:
        self.response.write('''
            Welcome to our site, %s!  Please sign up! <br>
            <form method="post" action="/">
            <input type="text" name="first_name">
            <input type="text" name="last_name">
            <input type="submit">
            </form><br> %s <br>
            ''' % (email_address, signout_link_html))
    else:
      # If the user isn't logged in...
      login_url = users.create_login_url('/')
      login_html_element = '<a href="%s">Sign in</a>' % login_url
      # Prompt the user to sign in.
      self.response.write('Please log in.<br>' + login_html_element)

  def post(self):
    # Code to handle a first-time registration from the form:
    user = users.get_current_user()
    cssi_user = CssiUser(
        first_name=self.request.get('first_name'),
        last_name=self.request.get('last_name'),
        email=user.nickname())
    cssi_user.put()
    self.response.write('Thanks for signing up, %s! <br><a href="/">Home</a>' %
        cssi_user.first_name)

class OutfitHandler(webapp2.RequestHandler):
    def get(self):
        make_template = jinja_current_dir.get_template('templates/make-fits.html') #html page to be used
        self.response.write(make_template.render())

class shirt(webapp2.RequestHandler):
    def get(self):
        shirt_template = jinja_current_dir.get_template('templates/shirts.html') #html page to be used

        shirts_list = get_shirts()


        jinja_dict = {
            'shirts': shirts_list
        }
        print(jinja_dict)
        self.response.write(shirt_template.render(jinja_dict))

        # self.response.write(json.dumps(objects_list))

class pant(webapp2.RequestHandler):
    def get(self):
        pant_template = jinja_current_dir.get_template('templates/pants.html') #html page to be used

        pant_list = get_pants()


        jinja_dict = {
            'pants': pant_list
        }
        print(jinja_dict)
        self.response.write(pant_template.render(jinja_dict))

class jackets(webapp2.RequestHandler):
    def get(self):
        jacket_template = jinja_current_dir.get_template('templates/jackets.html') #html page to be used

        jacket_list = get_jacket()


        jinja_dict = {
            'jacket': jacket_list
        }
        print(jinja_dict)
        self.response.write(jacket_template.render(jinja_dict))

class shoes(webapp2.RequestHandler):
    def get(self):
        shoes_template = jinja_current_dir.get_template('templates/shoes.html') #html page to be used

        shoes_list = get_shoes()


        jinja_dict = {
            'shoes': shoes_list
        }
        print(jinja_dict)
        self.response.write(shoes_template.render(jinja_dict))

        # self.response.write(json.dumps(objects_list))


app = webapp2.WSGIApplication([
  ('/sign-in', MainHandler),
  ('/upload', Upload),
  ('/all_clothes', AllClothes),
  ('/make_outfits', OutfitHandler),
  ('/about_us', about),
  ('/welcome', welcome),
  # ('/shirtsjson', ShirtsJSON),
  ('/search', search),
  ('/shirt', shirt),
  ('/pant', pant),
  ('/jackets', jackets),
  ('/shoes', shoes),
], debug=True)
