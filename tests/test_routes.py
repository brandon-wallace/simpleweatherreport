from application import create_app
from application.routes import fahrenheit_to_celcius


def test_fahrenheit_to_celcius():
    '''Test conversion to celcius'''

    assert fahrenheit_to_celcius(43) == (43 - 32) / 1.8


def test_index_page():
    '''Test index page route'''

    app = create_app()

    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
