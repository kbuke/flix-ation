from flask import make_response, session, request
from flask_restful import Resource
from config import db 
from models.fave_cinemas import FaveCinemaModel
from models.user import IndividualModel, CinemaModel


class FaveCinemaList(Resource):
    def get(self):
        fave_cinemas = [fave_cinema.to_dict() for fave_cinema in FaveCinemaModel.query.all()]
        return fave_cinemas
    
    def post(self):
        json = request.get_json()

        user_id = json.get("userId")
        cinema_id = json.get("cinemaId")
        
        # ensure user hasnt already favourited the cinema
        existing_fave = FaveCinemaModel.query.filter_by(individual_id=user_id, cinema_id=cinema_id).first()

        if existing_fave:
            return {"error": "You have already favourited this cinema"}

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

class FaveCinema(Resource):
    def get(self, id):
        fave_cinema = FaveCinemaModel.query.filter(FaveCinemaModel.id==id).first()
        if fave_cinema:
            return fave_cinema.to_dict(), 200
        else:
            return {"error": "fave cinema not found"}, 404 
        
    def delete(self, id):
        fave_cinema = FaveCinemaModel.query.filter(FaveCinemaModel.id==id).first()
        if fave_cinema:
            db.session.delete(fave_cinema)
            db.session.commit()
            return {"message": "Fave cinema deleted"}
        else:
            return {"message": "Fave cinema not found"}, 404