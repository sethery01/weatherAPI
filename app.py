import requests
import json
from flask import Flask, send_from_directory, request

state_codes = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 
    'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 
    'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

app  = Flask(__name__)

@app.route('/')
def serve_static_html():
    return send_from_directory('./', 'index.html')

@app.route('/weather', methods=["GET"])
def consume_state_weather():
    state = request.args.get("state")

    # Invalid state or query
    if not state:
        message = "ERROR: No state code given"
        return message, 400
    elif state not in state_codes:
        message = "ERROR: Bad Request"
        return message, 400

    # Make request if above check(s) is passed
    response = requests.get("https://api.weather.gov/alerts/active/area/" + state)

    if response.status_code == 200:
        #alerts = []
        alerts_dict = {}
        for data in response.json()["features"]:
            alerts_dict[data["properties"]["headline"]] = data["properties"]["instruction"]
            #alerts.append(data["properties"]["instruction"])

        return alerts_dict, 200
    else:
        return "ERROR 404 NOT FOUND", 404
    
if __name__ == '__main__':
   app.run(host = "0.0.0.0", port=80)