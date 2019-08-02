import webapp2
import jinja2
import os
import json
import time
from ClothesModel import ourPics
from CSSIUser import CssiUser
from ClothesModel import Outfit
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

from get_all_clothes import AllClothes, ViewMadeFits
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
        <head>
              <link rel="stylesheet" href="../stylesheets/style.css">
        <title>Sign out</title>
        </head>
        <header class="topnav">
          <img src="https://cdn1.iconfinder.com/data/icons/office-web/128/office-94-512.png">
          <nav>
            <ul>
              <li><a href="/welcome">Home</a></li>
              <li><a href="/all_clothes">Wardrobe</a></li>
              <li><a href="/upload">Upload</a></li>
              <li><a href="/make_outfits">Make Outfit</a></li>
              <li><a href="/about_us">About</a></li>
              <li><a href="/sign-in">Sign Out</a></li>
              <li>
              <form class="changepage" action="/search" method="get">
                 <div class="input-field">
                     <input id="search" name="search" type="search" required>
                     <label class="label-icon" for="search">
                     <i class="material-icons">search</i></label>
                  </div>
              </form>
              </ul>
            </nav>
            </header>
            <body style="background-color: powderblue">
            <br>
            <br>
            <br>
            <br>
            <h1 style="text-align: center;">Would you like to sign out? </h1>  <center> <a href=" %s "> <button id= "sign_out_button" type="button">Sign out!</button></a> <center> <br>  <br>
            ''' % (users.create_logout_url('/')))
    else:
        # If the user isn't logged in...
        login_url = users.create_login_url('/')
        self.redirect(login_url)          #SIgn in HTML


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
            self.response.write(make_template.render(dict))
        else:
            # If the user isn't logged in...
            login_url = users.create_login_url('/welcome')
            # Prompt the user to sign in.
            self.redirect(login_url)



class shirt(webapp2.RequestHandler):
    def get(self):
        shirt_template = jinja_current_dir.get_template('templates/shirts.html') #html page to be used
        shirts_list = get_shirts()
        selected= "var_string"
        jinja_dict = {
            'shirts': shirts_list,
            'selected': selected
        }
        self.response.write(shirt_template.render(jinja_dict))
    def post(self):
        selected = self.request.get("{{selected}}")

    def post(self):
        selected = self.request.get("var_string")
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
        self.response.write(pant_template.render(jinja_dict))

class jackets(webapp2.RequestHandler):
    def get(self):
        jacket_template = jinja_current_dir.get_template('templates/jackets.html') #html page to be used

        jacket_list = get_jacket()

        jinja_dict = {
            'jackets': jacket_list
        }

        self.response.write(jacket_template.render(jinja_dict))

class shoes(webapp2.RequestHandler):
    def get(self):
        shoes_template = jinja_current_dir.get_template('templates/shoes.html') #html page to be used

        shoes_list = get_shoes()

        jinja_dict = {
            'shoes': shoes_list,
        }

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
        if not 'outfit' in self.session or self.request.get('clear_outfit') == 'true':
            self.session['outfit'] = []

        outfit = self.session['outfit']
        if 'add' in self.request.GET:
            outfit.append(self.request.get('add'))
        self.session['outfit'] = outfit
        clothing_urls = []
        for item in self.session['outfit']:
            item_key = ndb.Key(urlsafe = item)
            clothing_urls.append(item_key.get())

        outfit_template = jinja_current_dir.get_template('templates/made-fits.html') #html page to be used

        jinja_dict = {
            'outfits': clothing_urls,
            }
        self.response.write(outfit_template.render(jinja_dict))

    def post(self):
        ndb.Key(urlsafe = self.session['outfit'][0]).get()
        outfit_keys = [ndb.Key(urlsafe = x) for x in self.session['outfit']]
        result = Outfit(user = users.get_current_user().email())
        for key in outfit_keys:
            item = key.get()

            if item.categories == 'shirt':
                result.top = key
            if item.categories == 'jacket':
                result.outerwear = key
            if item.categories == 'pants':
                result.bottoms = key
            if item.categories == 'shoes':
                result.shoes = key
        result.put()
        time.sleep(0.1)
        self.session['outfit'] = []
        self.redirect('/view-made-fits')

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
  ('/view-made-fits', ViewMadeFits),
  # ('/made_outfits', MadeOutfits),
  ('/cart', OutfitCart),
], config=config, debug=True)
