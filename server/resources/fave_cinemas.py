from flask import make_response, session, request
from flask_restful import Resource
from config import db 
from models.fave_cinemas import FaveCinemaModel


class FaveCinemaList(Resource):
    def post(self):
        json = request.get_json()

        if json:
            try:
                new_fave_cinema = FaveCinemaModel(
                    individual_id = json.get("userId"),
                    cinema_id = json.get("cinemaId")
                )
                db.session.add(new_fave_cinema)
                db.session.commit()
                return new_fave_cinema.to_dict()
            except ValueError as e:
                return {"error": [str(e)]}
        else:
            return {"error": "No data found"}, 404