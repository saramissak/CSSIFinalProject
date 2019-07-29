from google.appengine.ext import ndb

class Clothes(ndb.Model):
    img_url = ndb.StringProperty(required = True)
    article_name = ndb.StringProperty(required = True)
    article_description = ndb.StringProperty(required = False)
    organization = ndb.StringProperty(required = False)

    def getLines(self):
        return self.line1 + " " + self.line2
