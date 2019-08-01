import jinja2
import webapp2
import os
import time
from ClothesModel import Clothes
from CSSIUser import CssiUser

from google.appengine.api import users
from google.appengine.ext import ndb


the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Upload(webapp2.RequestHandler):
    def post(self):
        count = 0
        user = users.get_current_user()

        for ele in Clothes.query().fetch():
            count += 1
        #get information from the form
        img_url = self.request.get("img_url")
        article_name = self.request.get("article_name")
        article_description = self.request.get("article_description")
        categories = self.request.get("categories")
        personal_organization = self.request.get("personal_organization")

        #add to database
        user_clothes = Clothes(user= user.email(),img_url = img_url, article_name = article_name, article_description = article_description, categories=categories, personal_organization = personal_organization, number = count)
        user_clothes.put()
        time.sleep(.1)
        #chane the page
        self.redirect('/all_clothes')

    def get(self):

        user = users.get_current_user()
        # If the user is logged in...
        if user:
            upload_template = the_jinja_env.get_template('templates/upload.html') #html page to be used
            clothes_query = Clothes.query()
            clothes_fetch = clothes_query.fetch()
            self.response.write(upload_template.render())

            signout_link_html = '<a href="%s">sign out</a>' % (
              users.create_logout_url('/'))
            email_address = user.nickname()
            cssi_user = CssiUser.query().filter(CssiUser.email == email_address).get()
        else:
            # If the user isn't logged in...
            login_url = users.create_login_url('/')
            login_html_element = '<a href="%s">Sign in</a>' % login_url
            # Prompt the user to sign in.
            self.response.write('Please log in.<br>' + login_html_element)
