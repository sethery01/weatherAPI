from typing import Union
from fastapi import FastAPI 
from fastapi.responses import HTMLResponse
import os
import requests
import uvicorn

state_codes = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 
    'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 
    'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

app = FastAPI()

# Display static html
@app.get("/", response_class=HTMLResponse)
async def read_index():
    # Read the contents of the index.html file
    with open(os.path.join("static", "index.html"), "r") as file:
        return HTMLResponse(content=file.read())

# Return server health check
@app.get("/health")
async def return_health():
    return "udlsethtst02.vuhl.root.mrc.local", 200


# Return alerts with state param
@app.get('/alerts')
# read_item from fastAPI - Gets the state query param
async def read_item(state: str):

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
        alerts_dict = {}
        for data in response.json()["features"]:
            alerts_dict[data["properties"]["headline"]] = data["properties"]["instruction"]
        return alerts_dict, 200
    else:
        return "ERROR 404 NOT FOUND", 404


# Return a link to weather forecast 
# @app.get("/forecast")
# # read_item from fastAPI - Gets the county query param
# async def read_item(county: str):
    
#     if not county:
#         message = "ERROR: No county parameter given"
#         return message, 400
    
#     return -1

def main():
    uvicorn.run(app, host="0.0.0.0", port=443, ssl_keyfile='./key.key', ssl_certfile='./cert.crt')

# Main calling function
if __name__ == "__main__":
    main()