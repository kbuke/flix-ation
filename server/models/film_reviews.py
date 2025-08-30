# An individual can review many films
# A film can be reviewd by many individuals
import requests

from flask import current_app

from config import db 
from sqlalchemy_serializer import SerializerMixin

from dotenv import load_dotenv

import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

class ReviewModel(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key = True)
    rating = db.Column(db.Integer, nullable=False)
    review_title = db.Column(db.String, nullable=True)
    review = db.Column(db.String, nullable=True)

    individual_id = db.Column(db.Integer, db.ForeignKey("individuals.id"), nullable=False)
    individual = db.relationship("IndividualModel", back_populates="reviews")

    film_api_id = db.Column(db.Integer, nullable = False)

    serialize_rules = (
        "-individual",
    )

    @property
    def film_details(self):
        url = f"https://streaming-availability.p.rapidapi.com/shows/{self.film_api_id}"
        headers = {
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
        }
        resp = requests.get(url, headers=headers)
        if resp.ok:
            data = resp.json()
            return {
                "title": data.get("title"),
                "poster": (
                    data.get("imageSet", {})
                        .get("verticalPoster", {})
                        .get("w240")
                )
            }
        return {}