from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import requests

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

TOKEN = '5PAGVY4ZL5AHORZPQ64P'
headers = {'Authorization': 'Bearer ' + TOKEN}

@app.route('/')
def hello_world():
    return 'Go to /events/LOCATION/PAGE to browse upcoming events.'

@app.route('/events/<location>/<page>')
@cross_origin()
def get_events(location, page):
	r = requests.get('https://www.eventbriteapi.com/v3/events/search?location.address=' + location + '&expand=ticket_classes&page=' + str(page), headers = headers)
	return jsonify(r.json())