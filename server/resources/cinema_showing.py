from flask import session, make_response, request
from flask_restful import Resource
from config import db 
from models.cinema_showing import CinemaShowingModel
from datetime import datetime

class CinemaShowingList(Resource):
    def post(self):
        json = request.get_json()

        if json:
            date = json.get("showDate")
            format_date = datetime.strptime(date, "%Y-%m-%d").date()

            time = json.get("startTime")
            format_time = datetime.strptime(time, "%H:%M").time()
            try:
                new_showing = CinemaShowingModel(
                    show_date = format_date,
                    screen = json.get("screen"),
                    start_time = format_time,
                    cinema_id = json.get("cinemaId"),
                    film_api_id = json.get("filmId")
                )
                db.session.add(new_showing)
                db.session.commit()
                return new_showing.to_dict(), 201 
            except ValueError as e:
                return {"error": [str(e)]}
        else:
            return {"error": "Failed to load json"}, 404