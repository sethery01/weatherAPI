from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
import uvicorn

# server URL: "udl01sethtst02.vuhl.root.mrc.local"

state_codes = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 
    'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 
    'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

# init the app
app = FastAPI()

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Display static html
@app.get("/", response_class=HTMLResponse)
async def read_index():
    # Read the contents of the index.html file
    with open(os.path.join("static", "index.html"), "r") as file:
        return HTMLResponse(content=file.read())

@app.get("/tts", response_class=HTMLResponse)
async def read_index():
    # Read the contents of the index.html file
    with open(os.path.join("static", "tts.html"), "r") as file:
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

    # Make request if above check(s) pass
    response = requests.get("https://api.weather.gov/alerts/active/area/" + state)

    if response.status_code == 200:
        alerts_dict = {}
        for data in response.json()["features"]:
            alerts_dict[data["properties"]["headline"]] = data["properties"]["instruction"]
        return alerts_dict, 200
    else:
        return "ERROR 404 NOT FOUND", 404


#Return a link to weather forecast 
@app.get("/forecast")
# read_item from fastAPI - Gets the county query param
async def read_item(state: str, county: str):
    
    if not state or not county:
        message = "ERROR: No state or county parameter given"
        return message, 400
    elif state not in state_codes:
        return "ERROR: Bad Request", 400
    
    # Make a get request for zones by county if above check(s) pass
    response = requests.get("https://api.weather.gov/zones/county")
    
    if response.status_code == 200:
        for data in response.json()["features"]:
            if state == data["properties"]["state"] and county == data["properties"]["name"]:
                dict_link =  data["properties"]["forecastOffices"]
                link = dict_link[0]
                response2 = requests.get(str(link))
                link = response2.json()["sameAs"]
                # Redirect the client to the obtained link
                return RedirectResponse(url=link)
        # If the loop completes without finding a match
        raise HTTPException(status_code=404, detail="ERROR 404 NOT FOUND")
    else:
        raise HTTPException(status_code=404, detail="ERROR 404 NOT FOUND")

def main():
    uvicorn.run(app, host="0.0.0.0", port=443, ssl_keyfile='./key.key', ssl_certfile='./cert.crt')

# Main calling function
if __name__ == "__main__":
    main()