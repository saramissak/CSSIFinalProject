import jinja2
import webapp2
import os

from CSSIUser import CssiUser
from ClothesModel import Clothes

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class search(webapp2.RequestHandler):
    def get(self):
        search_template = the_jinja_env.get_template('templates/search.html') #html page to be used

        self.response.write(search_template.render())
        aboutus_template = the_jinja_env.get_template('templates/aboutus.html') #html page to be used
        aboutus_template = the_jinja_env.get_template('templates/all-clothes.html') #html page to be used
        aboutus_template = the_jinja_env.get_template('templates/make-fits.html') #html page to be used
        aboutus_template = the_jinja_env.get_template('templates/search.html') #html page to be used
        aboutus_template = the_jinja_env.get_template('templates/upload.html') #html page to be used
        aboutus_template = the_jinja_env.get_template('templates/welcome.html') #html page to be used



        search = self.request.get("search")
        clothes_query = Clothes.query()
        list_of_search = []

        list_of_results = Clothes.query().filter(Clothes.article_description == search).fetch()
        list_len = len(list_of_results)
        if list_len > 0:
            list_of_results[0].article_description
        for match in list_of_results:
            if match.key not in list_of_search:
                list_of_search.append(match)


        list_of_results = Clothes.query().filter(Clothes.article_name == search).fetch()
        list_len = len(list_of_results)
        if list_len > 0:
            list_of_results[0].article_name
        for match in list_of_results:
            if match.key not in list_of_search:
                list_of_search.append(match)


        list_of_results = Clothes.query().filter(Clothes.categories == search).fetch()
        list_len = len(list_of_results)
        if list_len > 0:
            list_of_results[0].categories
        for match in list_of_results:
            if match.key not in list_of_search:
                list_of_search.append(match)

        list_of_results = Clothes.query().filter(Clothes.img_url == search).fetch()
        list_len = len(list_of_results)
        if list_len > 0:
            list_of_results[0].img_url
        for match in list_of_results:
            if match.key not in list_of_search:
                list_of_search.append(match)

        list_of_results = Clothes.query().filter(Clothes.personal_organization == search).fetch()
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
