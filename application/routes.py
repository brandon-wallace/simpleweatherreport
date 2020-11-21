import json
import pytz
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from datetime import datetime
from flask import render_template, request, redirect, url_for
from flask_babel import format_datetime
from application import app, babel, api_key
from application.forms import AddressForm

lon, lat = None, None


@babel.localeselector
def get_locale():
    '''Get locale of user'''

    return request.accept_languages.best_match(['en', 'de', 'fr', 'es'])


def find_location(addr):
    '''Get latitude and longitude'''

    try:
        geolocator = Nominatim(user_agent='application', timeout=3)
        return geolocator.geocode(addr)
    except (GeocoderTimedOut, GeocoderServiceError):
        return


@app.route('/', methods=['GET', 'POST'])
def index():
    '''Index route'''

    form = AddressForm()
    if form.validate_on_submit():
        return redirect(url_for('get_weather_report'))
    return render_template('index.html', form=form)


@app.route('/weather', methods=['GET', 'POST'])
def get_weather_report():
    '''Display local weather report based on geolocation'''

    form = AddressForm()
    addr = request.form.get('address')
    location = find_location(addr)

    if location is None:
        return render_template('index.html', form=form, message="Location Not Found")

    else:
        lat = location.latitude
        lon = location.longitude
        local_address = location.address
        url = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}&units=imperial'.format(lat, lon, api_key))

        if url.status_code == 200:
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
            daily_high = []
            daily_low = []
            daily_datetime = []

            current_temp = data['current']['temp']
            current_temp_c = (current_temp - 32) * 5.0 / 9.0
            current_forecast = data['current']['weather'][0]['description']
            tzone = data['timezone']
            current_low = data['daily'][0]['temp']['min']
            current_low_c = (current_low - 32) * 5.0 / 9.0
            current_high = data['daily'][0]['temp']['max']
            current_high_c = (current_high - 32) * 5.0 / 9.0
            sunrise = datetime.fromtimestamp(data['daily'][0]['sunrise'], tz=pytz.timezone(tzone)).strftime('%Hh:%Mm')
            sunset = datetime.fromtimestamp(data['daily'][0]['sunset'], tz=pytz.timezone(tzone)).strftime('%Hh:%Mm')

            for txt in data['hourly']:
                hours.append(datetime.fromtimestamp(txt['dt']).strftime("%H"))
                temps.append(txt['temp'])
                temps_celcius.append((int(txt['temp']) - 32) * 5.0 / 9.0)
                forecast.append(txt['weather'][0]['description'])
                humidity.append(txt['humidity'])
                wind_speed.append(txt['wind_speed'])
                visibility.append(txt['visibility'])
                pressure.append(txt['pressure'])

            for i in range(7):
                daily_high.append(data['daily'][i]['temp']['max'])
                daily_low.append(data['daily'][i]['temp']['min'])
                daily_datetime.append(datetime.fromtimestamp(data['daily'][i]['dt']).strftime('%a %b %d'))

                content = {
                    'daily_high': daily_high,
                    'daily_low': daily_low,
                    'daily_datetime': daily_datetime,
                    'sunrise': sunrise,
                    'sunset': sunset,
                    'local_address': local_address,
                    'lat': lat,
                    'lon': lon,
                    'current_temp': current_temp,
                    'current_temp_c': current_temp_c,
                    'current_forecast': current_forecast,
                    'timezone': tzone,
                    'current_low': current_low,
                    'current_low_c': current_low_c,
                    'current_high': current_high,
                    'current_high_c': current_high_c,
                    'hours': hours,
                    'temps': temps,
                    'temps_celcius': temps_celcius,
                    'forecast': forecast,
                    'humidity': humidity,
                    'wind_speed': wind_speed,
                    'visibility': visibility,
                    'pressure': pressure
                    }
    return render_template('weather.html', form=form, **content)
