import webapp2
from views import MainPage, CreateListing, DeleteListing, EditListing

app = webapp2.WSGIApplication([
        ('/', MainPage), 
        ('/create', CreateListing), 
        ('/edit/([\d]+)', EditListing),
        ('/delete/([\d]+)', DeleteListing)
        ],
        debug=True)
