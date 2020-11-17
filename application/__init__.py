import os
import json
from flask import Flask
from flask_babel import Babel
from datetime import datetime


app = Flask(__name__)
babel = Babel()

api_key = os.getenv('API_KEY')


def create_app():
    '''Initialize application'''

    app.config['DEBUG'] = False
    app.config['FLASK_ENV'] = os.getenv('FLASK_ENV')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'

    babel.init_app(app)

    return app


from application import routes
