import requests
from flask import Blueprint, jsonify, request
import os
from dotenv import load_dotenv
from flask_restful import Resource

movies_bp = Blueprint("movies", __name__)

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_HOST = "https://streaming-availability.p.rapidapi.com"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
}

class Film(Resource):
    def get(self, film_id):
        url = f"{API_HOST}/shows/{film_id}"
        response = requests.get(url, headers=headers)

        try:
            data = response.json()
        except Exception:
            return {"error": "Invalid JSON returned from API"}, 500
        
        if response.status_code == 200:
            return data, 200
        return {"error": f"Movie {film_id} not found"}, response.status_code

class FilmGenres(Resource):
    def get(self):
        url = f"{API_HOST}/genres"
        params = {"output_language": request.args.get("lang", "en")}
        response = requests.get(url, headers=headers, params=params)
        # breakpoint()

        try:
            data = response.json()
        except Exception:
            return {"error": "Invalid JSON returned from API"}, 500
        
        if response.status_code == 200:
            return data, 200
        return {"error": f"Genres not found"}, response.status_code