import jinja2
import os
import webapp2
from datetime import datetime
import unicodedata
from google.appengine.ext import db
from google.appengine.api import users

from models import SubletListing

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = \
    jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))


class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(
        self,
        filename,
        template_values,
        **template_args
        ):
        template = jinja_environment.get_template(filename)
        self.response.out.write(template.render(template_values))


class MainPage(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if user:            
            listings = SubletListing.gql("WHERE lister = :lister", lister=user.nickname())
            self.render_template('index.html', {'listings': listings,'user': user,'logout_url': users.create_logout_url("/")})
            
        else:
            self.redirect(users.create_login_url(self.request.uri))
                
class CreateListing(BaseHandler):
    def post(self):     
        n = SubletListing(lister = str(self.request.get('lister')),
                          street_name = str(self.request.get('street_name')),
                          city_name = str(self.request.get('city_name')),
                          state_name = str(self.request.get('state_name')),
                          start_date = datetime.strptime(str(self.request.get('start_date')),'%Y-%m-%d').date(),
                          end_date = datetime.strptime(str(self.request.get('end_date')),'%Y-%m-%d').date(),
                          price = float(str(self.request.get('price'))),
                          number_of_rooms = int(str(self.request.get('number_of_rooms'))),
                          number_of_bathrooms = float(str(self.request.get('number_of_bathrooms'))),
                          pets_allowed = str(self.request.get('pets_allowed')),
                          air_conditioning = str(self.request.get('air_conditioning')),
                          smoking_allowed = str(self.request.get('smoking_allowed')),
                          description = str(self.request.get('description')))
        n.put()
        return webapp2.redirect('/')

    def get(self):
        self.render_template('create.html', {'user': users.get_current_user().nickname()})


class EditListing(BaseHandler):
    def post(self, listing_id):
        iden = int(listing_id)
        listing = db.get(db.Key.from_path('SubletListing', iden))
        listing.lister = str(self.request.get('lister'))
        listing.street_name = str(self.request.get('street_name'))
        listing.city_name = str(self.request.get('city_name'))
        listing.state_name = str(self.request.get('state_name'))
        listing.start_date = datetime.strptime(str(self.request.get('start_date')),'%Y-%m-%d').date()
        listing.end_date = datetime.strptime(str(self.request.get('end_date')),'%Y-%m-%d').date()
        listing.price = float(str(self.request.get('price')))
        listing.number_of_rooms = int(str(self.request.get('number_of_rooms')))
        listing.number_of_bathrooms = float(str(self.request.get('number_of_bathrooms')))
        listing.pets_allowed = str(self.request.get('pets_allowed'))
        listing.air_conditioning = str(self.request.get('air_conditioning'))
        listing.smoking_allowed = str(self.request.get('smoking_allowed'))
        listing.description = str(self.request.get('description'))
        listing.put()
        return webapp2.redirect('/')
        
        
    def get(self, listing_id):
        iden = int(listing_id)
        listing = db.get(db.Key.from_path('SubletListing', iden))
        self.render_template('edit.html', {'listing': listing})


class DeleteListing(BaseHandler):
    def get(self, listing_id):
        iden = int(listing_id)
        listing = db.get(db.Key.from_path('SubletListing', iden))
        db.delete(listing)
        return webapp2.redirect('/')
