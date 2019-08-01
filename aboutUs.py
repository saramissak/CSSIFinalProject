import jinja2
import webapp2
import os

from ClothesModel import Clothes
from CSSIUser import CssiUser
from google.appengine.api import users



the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class about(webapp2.RequestHandler):
    def get(self):
        aboutus_template = the_jinja_env.get_template('templates/aboutus.html') #html page to be used
        self.response.write(aboutus_template.render())


class welcome(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            signout_link_html = '<a href="%s">sign out</a>' % (
                users.create_logout_url('/sign-in'))
            email_address = user.nickname()
            cssi_user = CssiUser.query().filter(CssiUser.email == email_address).get()
            welcome_template = the_jinja_env.get_template('templates/welcome.html') #html page to be used
            self.response.write(welcome_template.render())
        else:
           # If the user isn't logged in...
           login_url = users.create_login_url('/')
           login_html_element = '<a href="%s">Sign in</a>' % login_url
           # Prompt the user to sign in.
           self.response.write('Please log in.<br>' + login_html_element)
