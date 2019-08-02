import webapp2
import jinja2
import os
import json

from ClothesModel import ourPics
from CSSIUser import CssiUser
from ClothesModel import outfit
from makefits import get_shirts
from makefits import get_pants
from makefits import get_jacket
from makefits import get_shoes
# from makefits import get_outfits
from Search import search
from aboutUs import about
from aboutUs import welcome
from ClothesModel import Clothes
from Upload import Upload

from get_all_clothes import AllClothes
from makefits import select_clothing_piece

# from makefits import ShirtsJSON

from webapp2_extras import sessions

from google.appengine.api import users
from google.appengine.ext import ndb



jinja_current_dir = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

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
        # Offer a registration form for a first-time visitor:                  #SIGN OUT PAGE
        self.response.write('''
            <body style="background-color: skyblue">
            <p style="color:white"; text-align: "center"; border: "3px solid green">Would you like to sign out? </p> <br> %s <br>
            ''' % (signout_link_html))
    else:
      # If the user isn't logged in...
      login_url = users.create_login_url('/welcome')
      login_html_element = '<a href="%s">Sign in</a>' % login_url
      # Prompt the user to sign in.
      self.response.write('Please sign in.<br>' + login_html_element)          #SIgn in HTML


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
        user = users.get_current_user()
        if user:
            signout_link_html = '<a href="%s">sign out</a>' % (
              users.create_logout_url('/'))
            email_address = user.nickname()
            cssi_user = CssiUser.query()

            search = self.request.get("search")
            clothes_query = Clothes.query().filter(Clothes.user == user.email())
            list_of_search = []

            make_template = jinja_current_dir.get_template('templates/make-fits.html') #html page to be used
            list_of_results = clothes_query.filter(Clothes.personal_organization == search).fetch()
            list_len = len(list_of_results)
            if list_len > 0:
                list_of_results[0].personal_organization
            for match in list_of_results:
                if match.key not in list_of_search:
                    list_of_search.append(match)

            dict = {
                'img': list_of_search
            }
            print(list_of_search)
            self.response.write(make_template.render(dict))
        else:
            # If the user isn't logged in...
            login_url = users.create_login_url('/')
            login_html_element = '<a href="%s">Sign in</a>' % login_url
            # Prompt the user to sign in.


class shirt(webapp2.RequestHandler):
    def get(self):
        shirt_template = jinja_current_dir.get_template('templates/shirts.html') #html page to be used
        shirts_list = get_shirts()
        selected= "var_string"
        jinja_dict = {
            'shirts': shirts_list,
            'selected': selected
        }
        print(jinja_dict)
        self.response.write(shirt_template.render(jinja_dict))
    def post(self):
        selected = self.request.get("{{selected}}")

    def post(self):
        selected = self.request.get("var_string")
        print("Selected outfit " + selected)
        user_outfits = outfit(top = selected)
        user_outfits.put()
        self.redirect('/made_outfits')

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
            'jackets': jacket_list
        }
        print(jinja_dict)
        self.response.write(jacket_template.render(jinja_dict))

class shoes(webapp2.RequestHandler):
    def get(self):
        shoes_template = jinja_current_dir.get_template('templates/shoes.html') #html page to be used

        shoes_list = get_shoes()

        jinja_dict = {
            'shoes': shoes_list,
        }
        print(jinja_dict)
        self.response.write(shoes_template.render(jinja_dict))

        # self.response.write(json.dumps(objects_list))

class indexHandler(webapp2.RequestHandler):
    def get(self):
        index_template = jinja_current_dir.get_template('templates/index.html') #html page to be used
        self.response.write(index_template.render())

# class MadeOutfits(webapp2.RequestHandler):
#     def get(self):
#         made_fits_template = jinja_current_dir.get_template('templates/made-fits.html')
#         outfit_list = get_outfits()
#
#         outfit_dict = {
#             'outfits': outfit_list
#         }
#         self.response.write(made_fits_template.render(outfit_dict))

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

class OutfitCart(BaseHandler):
    def get(self):
        if not 'outfit' in self.session:
            self.session['outfit'] = []
        self.session['outfit'].append(self.request.get('add'))
        clothing_urls = []
        for item in self.session['outfit']:
            item_key = ndb.Key(urlsafe = item)
            print(item)
            clothing_urls.append(item_key.get())

        outfit_template = jinja_current_dir.get_template('templates/made-fits.html') #html page to be used

        jinja_dict = {
            'outfits': clothing_urls,
            }

        print(jinja_dict)
        self.response.write(outfit_template.render(jinja_dict))




config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

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
  ('/', indexHandler),
  # ('/made_outfits', MadeOutfits),
  ('/cart', OutfitCart),
], config=config, debug=True)
