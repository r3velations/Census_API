import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import httpx
import secrets

app = FastAPI()
api_key = secrets.get_api_key()


@app.get("/")
def get_root():
    return "This is an API to return data from the US Census Bureau databases."


# Working
@app.get("/help", response_class=HTMLResponse)
def provide_help_response():
    return """ 
          <html>
            <a href="http://127.0.0.1:8000/docs">Swagger Doc</a>
          </html>
        """


# Working
@app.get("/states/statecodes")
def list_state_codes():
        base_url = "https://api.census.gov/data/2020/dec/ddhca"
        response = requests.get(f"{base_url}?get=NAME&for=state:*&key={api_key}").json()
        return response

# Working
@app.get("/counties/countycodes/{state_code}")
def list_county_codes(state_code):
    base_url = "https://api.census.gov/data/2020/dec/ddhca"
    response = requests.get(
        f"{base_url}?get=NAME&for=county:*&in=state:{state_code}&key={api_key}"
    ).json()
    return response


# Working
@app.get("/cities/citycodes/{state_code}")
def list_city_codes(state_code):
    base_url = base_url = "https://api.census.gov/data/2020/dec/ddhca"
    response = requests.get(
        f"{base_url}?get=NAME&for=place:*&in=state:{state_code}&key={api_key}"
    ).json()
    return response


# Working
@app.get("/cities/population/{city_code}/{state_code}")
def get_population_city(city_code, state_code):
    base_url = base_url = "https://api.census.gov/data/2020/dec/ddhca"
    response = requests.get(
        f"{base_url}?get=NAME,T01001_001N&for=place:{city_code}&in=state:{state_code}&key={api_key}"
    ).json()
    return {
        "census_api_url": f"{base_url}?get=NAME,T01001_001N&for=place:{city_code}&in=state:{state_code}&key=<insert_your_own_api_key>",
        "city_name: ": response[1][0],
        "population total: ": response[1][1],
    }


# Working
@app.get("/states/population/{state_code}")
def get_population_state(state_code):
    response = requests.get(
        f"https://api.census.gov/data/2021/pep/population?get=NAME,POP_2021&for=state:{state_code}&key={api_key}"
    ).json()
    return {"state: ": response[1][0], "population: ": response[1][1]}


# Broken unable to get county level data with this api
# @app.get("/counties/population/{county_code}/{state_code}")
# def get_population_county(county_code, state_code):
#     api_key = secrets.get_api_key()
#     response = requests.get(
#         f"https://api.census.gov/data/2021/pep/population?get=NAME,POP_2021&for=county:{county_code}&in=state:{state_code}&key={api_key}"
#     ).json()
#     return {
#         "county name and state: ": response[1][1],
#         "population: ": response[1][0],
#     }


# Asynchronous Example == not working --> use httpx
