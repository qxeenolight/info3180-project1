import base64
import os
from app import app
from . import db
# from werkzeug.security import generate_password_hash

class Property(db.Model):
    __tablename__ = 'property'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    location = db.Column(db.String(120))
    numrooms = db.Column(db.String(80))
    numbathrooms = db.Column(db.String(80))
    price = db.Column(db.String(255))
    property_type = db.Column(db.String(80))
    description = db.Column(db.String(1024))
    filename = db.Column(db.String(255))

    def __init__(self, title, location, numrooms, numbathrooms, price, property_type, description, filename):
        self.title = title
        self.location = location
        self.numrooms = numrooms
        self.numbathrooms = numbathrooms
        self.price = price
        self.property_type = property_type
        self.description = description
        self.filename = filename

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicodedata(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def get_image_url(self):
        with open(os.path.join(app.config['UPLOAD_FOLDER'], self.filename), 'rb') as img_file:
            encoded_image = base64.b64encode(img_file.read()).decode('utf-8')
        return f'data:image/jpeg;base64,{encoded_image}'
    
    def __repr__(self):
        return '<Property %r>' % (self.title)