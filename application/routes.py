import json
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from datetime import datetime
from flask import render_template, request, redirect, url_for
from flask_babel import format_datetime
from application import app, babel, api_key
from application.forms import AddressForm
from application.json_data import weather_report

lon, lat = None, None


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['en', 'de', 'fr', 'es'])


def find_location(addr):
    try:
        return geolocator.geocode(addr)
    except GeocoderTimedOut as e:
        print(e)


@app.route('/', methods=['GET', 'POST'])
def index():
    '''Index route'''

    date_time = format_datetime(datetime.now())
    form = AddressForm()
    content = {
            'date_time': date_time,
            'form': form
            }
    return render_template('index.html', **content)


@app.route('/weather', methods=['POST'])
def get_local_weather():
    '''Display local weather report based of geolocation'''

    form = AddressForm()
    address = request.form['address']
    geolocator = Nominatim(user_agent='application', timeout=3)
    location = geolocator.geocode(address)
    if location is None:
        return render_template('index.html', message='Location not found')
    else:
        lat = location.latitude
        lon = location.longitude
        url = requests.get('https://api.darksky.net/forecast/{}/{},{}'.format(api_key, lat, lon))
        # if url.response == 200:
        report = url.text
        data = json.loads(report)
        json.dumps(data, ensure_ascii=False)
        temps = []
        temps_celcius = []
        hours = []
        forecast = []
        humidity = []
        wind_speed = []
        visibility = []
        pressure = []
        uv_index = []
        ozone = []
        date_time = datetime.now().strftime('%c')

        for txt in data['hourly']['data']:
            hours.append(datetime.fromtimestamp(txt['time']).strftime("%H"))
            temps.append(txt['temperature'])
            temps_celcius.append((int(txt['temperature']) - 32) * 5.0 / 9.0)
            forecast.append(txt['summary'].lower())
            humidity.append(txt['humidity'])
            wind_speed.append(txt['windSpeed'])
            uv_index.append(txt['uvIndex'])
            ozone.append(txt['ozone'])
            visibility.append(txt['visibility'])
            pressure.append(txt['pressure'])

            content = {
                    'date_time': date_time,
                    'hours': hours,
                    'temps': temps,
                    'temps_celcius': temps_celcius,
                    'forecast': forecast,
                    'humidity': humidity,
                    'wind_speed': wind_speed,
                    'uv_index': uv_index,
                    'ozone': ozone,
                    'visibility': visibility,
                    'pressure': pressure
                    }
        # return redirect(url_for('index'))
    return render_template('weather.html', lon=lon, lat=lat, form=form, **content)
