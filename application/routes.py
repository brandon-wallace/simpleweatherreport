import logging
import json
import pytz
import requests
from os import environ
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from datetime import datetime
from flask import render_template, request, redirect, url_for
from application import app, babel
from application.forms import AddressForm

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('error.log')
formatter = logging.Formatter('%(asctime)s: %(levelname)s: \
                              %(name)s: %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


@babel.localeselector
def get_locale():
    '''Get locale of user'''

    return request.accept_languages.best_match(['en', 'de', 'fr', 'es'])


def get_user_ip_address():
    '''Get the user's current location'''

    if 'X-Forwarded-For' in request.headers:
        ip_address = str(request.headers['X-Forwarded-For'])
    else:
        ip_address = str(request.environ.get('HTTP_X_REAL_IP',
                         request.remote_addr))

    if ip_address == '127.0.0.1':
        ip_address = requests.get('http://ipecho.net/plain')
        if ip_address.status_code != 200:
            logger.warning(f"Not able to get IP address.")
            ip_address = requests.get('http://ip.42.pl/raw')
        ip_address = ip_address.text
    return ip_address


def find_user_location(ip_addr):
    '''Get latitude and longitude from IP address'''

    url = requests.get(f'http://ip-api.com/json/{ip_addr}?fields=status,message,region,country,city,zip,lat,lon,timezone')
    if url.status_code == 200:
        data = json.loads(url.text)
        lat = data['lat']
        lon = data['lon']
        city = data['city']
        region = data['region']
        country = data['country']
        return lat, lon, city, region, country
    logger.error(f"An error has occurred: {lat} {lon} {city} {region} {country}.")
    return None


def geolocation_search(location):
    '''Get latitude and longitude from geolocation'''

    try:
        geolocator = Nominatim(user_agent='yourweather.cc', timeout=6)
        return geolocator.geocode(location)
    except (GeocoderTimedOut, GeocoderServiceError):
        logger.error(f"Geocode Error!", exc_info=True)
        return None


def get_weather_report(lat, lon):
    '''Retrieve weather report'''

    owm_api_key = environ.get('OWM_API_KEY')
    url = requests.get(f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={owm_api_key}&units=imperial')
    if url.status_code == 200:
        text = url.json()
        return text
    return None


@app.route('/', methods=['GET', 'POST'])
def index():
    '''Index route'''

    latitude, longitude, city, region, country = None, None, None, None, None
    form = AddressForm()
    ip_address = get_user_ip_address()
    latitude, longitude, city, region, country = find_user_location(ip_address)
    data = get_weather_report(latitude, longitude)
    icon_id = data['current']['weather'][0]['id']
    current_temp = data['current']['temp']
    current_forecast = data['current']['weather'][0]['description']
    current_low = data['daily'][0]['temp']['min']
    current_high = data['daily'][0]['temp']['max']
    current_weather = {
                 'icon_id': icon_id,
                 'current_temp': current_temp,
                 'current_forecast': current_forecast,
                 'current_low': current_low,
                 'current_high': current_high,
                 'city': city,
                 'region': region,
                 'country': country
                 }
    if form.validate_on_submit():
        return redirect(url_for('weather_report'))
    return render_template('index.html', form=form, **current_weather)


@app.route('/weather', methods=['GET', 'POST'])
def weather_report():
    '''Display local weather report based on geolocation'''

    form = AddressForm()

    address = request.form.get('address')
    print(address)
    location = geolocation_search(address)

    if location is None:
        return render_template('index.html', form=form,
                               message="Location Not Found")
    else:
        latitude = location.latitude
        longitude = location.longitude
        local_address = location.address
        data = get_weather_report(latitude, longitude)

        icon_id = data['current']['weather'][0]['id']
        temps = []
        hours = []
        forecast = []
        humidity = []
        wind_speed = []
        visibility = []
        pressure = []
        daily_high = []
        daily_low = []
        daily_datetime = []

        current_temp = data['current']['temp']
        current_forecast = data['current']['weather'][0]['description']
        tzone = data['timezone']
        current_low = data['daily'][0]['temp']['min']
        current_high = data['daily'][0]['temp']['max']
        sunrise = datetime.fromtimestamp(data['daily'][0]['sunrise'],
                                         tz=pytz.timezone(
                                         tzone)).strftime('%Hh:%Mm')
        sunset = datetime.fromtimestamp(data['daily'][0]['sunset'],
                                        tz=pytz.timezone(
                                        tzone)).strftime('%Hh:%Mm')

        for txt in data['hourly']:
            hours.append(datetime.fromtimestamp(txt['dt']).strftime("%H"))
            temps.append(txt['temp'])
            forecast.append(txt['weather'][0]['description'])
            humidity.append(txt['humidity'])
            wind_speed.append(txt['wind_speed'])
            visibility.append(txt['visibility'])
            pressure.append(txt['pressure'])

        for i in range(7):
            daily_high.append(data['daily'][i]['temp']['max'])
            daily_low.append(data['daily'][i]['temp']['min'])
            daily_datetime.append(datetime.fromtimestamp(
                                  data['daily'][i]['dt']).strftime(
                                  '%a %b %d'))

            content = {
                'latitude': latitude,
                'longitude': longitude,
                'local_address': local_address,
                'icon_id': icon_id,
                'daily_high': daily_high,
                'daily_low': daily_low,
                'daily_datetime': daily_datetime,
                'sunrise': sunrise,
                'sunset': sunset,
                'local_address': local_address,
                'current_temp': current_temp,
                'current_forecast': current_forecast,
                'timezone': tzone,
                'current_low': current_low,
                'current_high': current_high,
                'hours': hours,
                'temps': temps,
                'forecast': forecast,
                'humidity': humidity,
                'wind_speed': wind_speed,
                'visibility': visibility,
                'pressure': pressure
                }
    return render_template('weather.html', form=form, **content)


@app.errorhandler(404)
def page_not_found(error):
    '''404 page not found route'''

    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    '''500 page not found route'''

    return render_template('500.html'), 500
