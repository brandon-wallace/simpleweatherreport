import pytest
from application import create_app
from application.routes import fahrenheit_to_celcius

app = create_app()


@pytest.fixture()
def client():
    '''Client for testing routes'''

    with app.test_client() as client:

        yield client


def test_fahrenheit_to_celcius():
    '''Test conversion to celcius'''

    assert fahrenheit_to_celcius(43) == (43 - 32) / 1.8


def test_index_page(client):
    '''Test index page route'''

    response = client.get('/')
    assert response.status_code == 200
