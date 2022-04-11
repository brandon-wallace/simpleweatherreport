from os import environ, urandom
from flask import Flask
from flask_babel import Babel

app = Flask(__name__)
babel = Babel()


def create_app():
    '''Initialize application'''

    app.config['DEBUG'] = False
    app.config['FLASK_ENV'] = environ.get('FLASK_ENV')
    app.config['SECRET_KEY'] = urandom(32)
    app.config['OWM_API_KEY'] = environ.get('OWM_API_KEY')
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'

    babel.init_app(app)

    from application import routes

    return app
