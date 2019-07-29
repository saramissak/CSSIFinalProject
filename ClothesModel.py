from google.appengine.ext import ndb

class Clothes(ndb.Model):
    img_url = ndb.StringProperty()
    article_name = ndb.StringProperty()
    article_description = ndb.StringProperty()
    organization = ndb.StringProperty()

    def getLines(self):
        return self.line1 + " " + self.line2
