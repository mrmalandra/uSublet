from google.appengine.ext import db
#from django.contrib.auth.models import User, UserManager

class SubletListing(db.Model):
    lister = db.StringProperty()    
    street_name = db.StringProperty()
    city_name = db.StringProperty()
    state_name = db.StringProperty()    
    start_date = db.DateProperty()
    end_date = db.DateProperty()
    price = db.FloatProperty()  
    number_of_rooms = db.IntegerProperty()
    number_of_bathrooms = db.FloatProperty()
    pets_allowed = db.StringProperty()
    air_conditioning = db.StringProperty()
    smoking_allowed = db.StringProperty()
    description = db.StringProperty(multiline=True)

## Extending the User Profile to include more fields
#class UserProfile(models.Model):
#    user = models.ForeignKey(User,unique=True)
#    nickname = models.CharField(max_length=50)
#    email = models.CharField(max_length=50)
#    school = models.CharField(max_length=50)
    
    
