import jinja2
import webapp2
import os

from ClothesModel import Clothes

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class AllClothes(webapp2.RequestHandler):
    def get(self):
        upload_template = the_jinja_env.get_template('templates/all-clothes.html') #html page to be used
        all_clothes_template = the_jinja_env.get_template('templates/click-image.js') #html page to be used


        clothes_query = Clothes.query()
        clothes_fetch = clothes_query.fetch()
        selected= "var_string"
        # count = "count"

        the_variable_dict = {
            'all_clothes': clothes_fetch,
            'selected': selected,
            # 'counter': count
        }
        self.response.write(upload_template.render(the_variable_dict))
