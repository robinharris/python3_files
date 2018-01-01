import requests
import json
from datetime import datetime

location = 'Hull'
#c689e5002a05621f028043404458059f

url = 'http://api.openweathermap.org/data/2.5/weather?q=' + location + '&appid=c689e5002a05621f028043404458059f&units=metric'

r = requests.get(url)
response = json.loads(r.content)
print(response)
time = datetime.utcfromtimestamp(response['dt'])
print('Temperature in {} at {} is {}'.format(location, time, response['main']['temp']))
sunrise = datetime.utcfromtimestamp(response['sys']['sunrise'])
sunset = datetime.utcfromtimestamp(response['sys']['sunset'])
print('Sunrise was at {} and sunset at {}'.format(sunrise, sunset))