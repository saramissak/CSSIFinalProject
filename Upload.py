import jinja2
import webapp2
import os

from ClothesModel import Clothes


the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Upload(webapp2.RequestHandler):
    def post(self):
        count = 0
        for ele in Clothes.query().fetch():
            count += 1
        img_url = self.request.get("img_url")
        article_name = self.request.get("article_name")
        article_description = self.request.get("article_description")
        categories = self.request.get("categories")
        personal_organization = self.request.get("personal_organization")

        #add to database
        user_clothes = Clothes(img_url = img_url, article_name = article_name, article_description = article_description, categories=categories, personal_organization = personal_organization, number = count)
        user_clothes.put()

        self.redirect('/welcome')



    def get(self):
        upload_template = the_jinja_env.get_template('templates/upload.html') #html page to be used
        clothes_query = Clothes.query()
        clothes_fetch = clothes_query.fetch()

        the_variable_dict = {
            #'key': variable
        }
        self.response.write(upload_template.render(the_variable_dict))
