from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


class AddressForm(FlaskForm):
    '''Address form'''

    address = StringField('Address', validators=[InputRequired()])
    submit = SubmitField('get location')
