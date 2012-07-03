import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
from views import MainPage, CreateListing, DeleteListing, EditListing

app = webapp2.WSGIApplication([
        ('/', MainPage), 
        ('/create', CreateListing), 
        ('/edit/([\d]+)', EditListing),
        ('/delete/([\d]+)', DeleteListing)
        ],
        debug=True)

def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
