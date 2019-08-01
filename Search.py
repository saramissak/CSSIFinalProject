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

class search(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        # If the user is logged in...
        if user:
            signout_link_html = '<a href="%s">sign out</a>' % (
              users.create_logout_url('/sign-in'))
            email_address = user.nickname()
            cssi_user = CssiUser.query().filter(CssiUser.email == email_address).get()
            search_template = the_jinja_env.get_template('templates/search.html') #html page to be used

            self.response.write(search_template.render())
            aboutus_template = the_jinja_env.get_template('templates/aboutus.html') #html page to be used
            aboutus_template = the_jinja_env.get_template('templates/all-clothes.html') #html page to be used
            aboutus_template = the_jinja_env.get_template('templates/make-fits.html') #html page to be used
            aboutus_template = the_jinja_env.get_template('templates/search.html') #html page to be used
            aboutus_template = the_jinja_env.get_template('templates/upload.html') #html page to be used
            aboutus_template = the_jinja_env.get_template('templates/welcome.html') #html page to be used

            search = self.request.get("search")
            clothes_query = Clothes.query().filter(Clothes.user == user.email())
            list_of_search = []

            list_of_results = clothes_query.filter(Clothes.article_description == search).fetch()
            list_len = len(list_of_results)
            if list_len > 0:
                list_of_results[0].article_description
            for match in list_of_results:
                if match.key not in list_of_search:
                    list_of_search.append(match)


            list_of_results = clothes_query.filter(Clothes.article_name == search).fetch()
            list_len = len(list_of_results)
            if list_len > 0:
                list_of_results[0].article_name
            for match in list_of_results:
                if match.key not in list_of_search:
                    list_of_search.append(match)


            list_of_results =clothes_query.filter(Clothes.categories == search).fetch()
            list_len = len(list_of_results)
            if list_len > 0:
                list_of_results[0].categories
            for match in list_of_results:
                if match.key not in list_of_search:
                    list_of_search.append(match)

            list_of_results = clothes_query.filter(Clothes.img_url == search).fetch()
            list_len = len(list_of_results)
            if list_len > 0:
                list_of_results[0].img_url
            for match in list_of_results:
                if match.key not in list_of_search:
                    list_of_search.append(match)

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
            self.response.write(search_template.render(dict))
        else:
            # If the user isn't logged in...
            login_url = users.create_login_url('/')
            login_html_element = '<a href="%s">Sign in</a>' % login_url
            # Prompt the user to sign in.
            self.response.write('Please log in.<br>' + login_html_element)
