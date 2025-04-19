from flask import Flask
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

OPEN_BREWERY_API_URL = "https://api.openbrewerydb.org/v1/breweries"

@app.route("/")
def root():
    return "Welcome to the Brewery App backend."

@app.route("/breweries")
def get_breweries():
    """
    Fetches a list of breweries from the Open Brewery DB API.
    Returns a JSON response with the list of breweries.
    """
    try:
        response = requests.get(OPEN_BREWERY_API_URL)
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500
    return response.json()

if __name__ == "__main__":
    app.run(debug=True)