from application.routes import fahrenheit_to_celcius


def test_fahrenheit_to_celcius():
    '''Test conversion to celcius'''

    assert fahrenheit_to_celcius(43) == (43 - 32) / 1.8
