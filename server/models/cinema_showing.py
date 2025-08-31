from sqlalchemy_serializer import SerializerMixin
from config import db 
from datetime import date, time
from config import Api

from dotenv import load_dotenv
import os, requests

load_dotenv()

API_KEY = os.getenv("API_KEY")

class CinemaShowingModel(db.Model, SerializerMixin):
    __tablename__ = "cinema_showings"

    id = db.Column(db.Integer, primary_key = True)
    show_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    # end_time = db.Column(db.Time, nullable=False, server_default="")
    screen = db.Column(db.Integer, nullable=False)

    cinema_id = db.Column(db.Integer, db.ForeignKey("cinemas.id"), nullable=False)
    cinema = db.relationship("CinemaModel", back_populates="showings")

    film_api_id = db.Column(db.Integer, nullable=False)

    serialize_rules = (
        "-cinema",
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

            # convert minutes to time format
            runtime_minutes = data.get("runtime")
            hours, mins = divmod(runtime_minutes, 60)
            runtime_str = f"{hours}h {mins}m" if hours else f"{mins}m"

            return{
                "title": data.get("title"),
                "poster": (
                    data.get("imageSet", {})
                        .get("verticalPoster", {})
                        .get("w240")
                ),
                "runtime": runtime_str
            }
        return {}
