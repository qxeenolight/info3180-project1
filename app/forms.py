from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import InputRequired

class PropertyForm(FlaskForm):
    # Text Fields
    title = StringField('Title', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])    
    numrooms = StringField('No. of Rooms', validators=[InputRequired()])
    numbathrooms = StringField('No. of Bathrooms', validators=[InputRequired()])
    price = StringField('Price', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])

    # Select Fields
    propertytypes = ['House', 'Apartment']
    propertytype = SelectField('Property Type', choices=propertytypes, validators=[InputRequired()])
    
    # File Upload
    photo = FileField('Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])