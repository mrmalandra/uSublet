import jinja2
import os
import webapp2
from datetime import datetime
import unicodedata
from google.appengine.ext import db

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
        listings = SubletListing.all()
        self.render_template('index.html', {'listings': listings})


class CreateListing(BaseHandler):

    def post(self):     
        n = SubletListing(lister = self.request.get('lister'),
                          street_name = unicodedata.normalize('NFKD', self.request.get('street_name')).encode('ascii','ignore'),
                          city_name = unicodedata.normalize('NFKD', self.request.get('city_name')).encode('ascii','ignore'),
                          state_name = unicodedata.normalize('NFKD', self.request.get('state_name')).encode('ascii','ignore'),
                          start_date = datetime.strptime(unicodedata.normalize('NFKD', self.request.get('start_date')).encode('ascii','ignore'),'%Y-%m-%d').date(),
                          end_date = datetime.strptime(unicodedata.normalize('NFKD', self.request.get('end_date')).encode('ascii','ignore'),'%Y-%m-%d').date(),
                          price = float(unicodedata.normalize('NFKD', self.request.get('price')).encode('ascii','ignore').strip()),
                          number_of_rooms = int(self.request.get('number_of_rooms').strip()) if self.request.get('number_of_rooms').isdigit() else 1,
                          number_of_bathrooms = float(self.request.get('number_of_bathrooms').strip()) if self.request.get('number_of_bathrooms').isdigit() else 1.0,
                          pets_allowed = self.request.get('pets_allowed'),
                          air_conditioning = self.request.get('air_conditioning'),
                          smoking_allowed = self.request.get('smoking_allowed'),
                          description = self.request.get('description'))
        n.put()
        return webapp2.redirect('/')

    def get(self):
        self.render_template('create.html', {})


class EditListing(BaseHandler):

    def post(self, listing_id):
        iden = int(listing_id)
        listing = db.get(db.Key.from_path('SubletListing', iden))
        listing.lister = unicodedata.normalize('NFKD',self.request.get('lister')).encode('ascii','ignore')
        listing.street_name = unicodedata.normalize('NFKD',self.request.get('street_name')).encode('ascii','ignore')
        listing.city_name = unicodedata.normalize('NFKD',self.request.get('city_name')).encode('ascii','ignore')
        listing.state_name = unicodedata.normalize('NFKD',self.request.get('state_name')).encode('ascii','ignore')
        listing.start_date = datetime.strptime(unicodedata.normalize('NFKD', self.request.get('start_date')).encode('ascii','ignore'),'%Y-%m-%d').date()
        listing.end_date = datetime.strptime(unicodedata.normalize('NFKD', self.request.get('end_date')).encode('ascii','ignore'),'%Y-%m-%d').date()
        listing.price = float(self.request.get('price')) if self.request.get('price').isdigit() else 200.0
        listing.number_of_rooms = int(self.request.get('number_of_rooms')) if self.request.get('number_of_rooms').isdigit() else 1
        listing.number_of_bathrooms = float(self.request.get('number_of_bathrooms')) if self.request.get('number_of_bathrooms').isdigit() else 1.0
        listing.pets_allowed = self.request.get('pets_allowed')
        listing.air_conditioning = self.request.get('air_conditioning')
        listing.smoking_allowed = self.request.get('smoking_allowed')
        listing.description = self.request.get('description')
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
