"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash

from app.forms import PropertyForm
from app.models import Property
from werkzeug.utils import secure_filename, send_from_directory

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


# -------------------------------------------
@app.route('/properties')
def properties():
    """Render website's properties page"""
    properties = Property.query.all()
    return render_template('properties.html', properties=properties)

@app.route('/properties/create', methods=['POST', 'GET'])
def create():
    """Render website's new property page."""
    form = PropertyForm() # Initialize Form
    if form.validate_on_submit():   
        # Create a new Property object with the form data
        file = form.photo.data

        new_property = Property(
            title=form.title.data,
            location=form.location.data,
            numrooms=form.numrooms.data,
            numbathrooms=form.numbathrooms.data,
            price=form.price.data,
            property_type=form.propertytype.data,
            description=form.description.data,
            filename=secure_filename(file.filename)
        )

        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        db.session.add(new_property)
        db.session.commit()
        flash('Property Added Successfully', 'success')

        return redirect(url_for('properties'))
    return render_template('newproperty.html', form = form)

@app.route('/properties/<propertyid>')
def listing(propertyid):
    """Render a property"""
    property = Property.query.get(propertyid)
    if property is None:
        page_not_found(400)  # Return a 404 error if property not found
    return render_template('listing.html', property=property)
# -------------------------------------------


###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
